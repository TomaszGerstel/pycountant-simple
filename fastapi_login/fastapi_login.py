import inspect
import os
import typing
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Collection, Dict, Union

import jwt
from fastapi import FastAPI, Request, Response
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from pydantic import parse_obj_as

from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login.secrets import Secret
from fastapi_login.utils import ordered_partial

SECRET_TYPE = Union[str, bytes]


class LoginManager(OAuth2PasswordBearer):
    """
    Attributes:
        secret (starlette.datastructures.Secret): The secret used to sign and decrypt the JWT
        algorithm (str): The algorithm used to decrypt the token defaults to ``HS256``
        token_url (str): The url where the user can login to get the token
        use_cookie (bool): Whether cookies should be checked for the token
        use_header (bool): Whether headers should be checked for the token
        pwd_context (passlib.CryptContext): Instance of ``passlib.CryptContext`` using bcrypt for
            convenient access to hashing and verifying passwords.
    """

    def __init__(
        self,
        secret: Union[SECRET_TYPE, Dict[str, SECRET_TYPE]],
        token_url: str,
        algorithm="HS256",
        cookie_name: str = "app-token-cookie",
        custom_exception: Exception = None,
        default_expiry: timedelta = timedelta(minutes=90),
    ):
        self.secret = parse_obj_as(Secret, {"algorithms": algorithm, "secret": secret})
        self._user_callback = None
        self.user_name = None
        # self.current_user_id = None
        # self.lump_sum_tax_rate = None
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        self.tokenUrl = token_url
        self.oauth_scheme = None
        self._not_authenticated_exception = (
            custom_exception or InvalidCredentialsException
        )
        self.cookie_name = cookie_name
        self.default_expiry = default_expiry

        if custom_exception is not None:
            super().__init__(tokenUrl=token_url, auto_error=False)
        else:
            super().__init__(tokenUrl=token_url, auto_error=True)

    @property
    def not_authenticated_exception(self):
        return self._not_authenticated_exception

    def user_loader(self, *args, **kwargs) -> Union[Callable, Awaitable]:

        def decorator(callback: Union[Callable, Awaitable]):
            self._user_callback = ordered_partial(callback, *args, **kwargs)
            return callback

        # If the only argument is also a callable this will lead to errors
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # No arguments have been passed and no empty parentheses have been used
            # this was the old way (before 1.7.0) of decorating the method.
            # Thus we assume the first argument is the actual callback.
            fn = args[0]
            # If we don't empty args the callback will be passed twice to ordered_partial
            args = ()
            decorator(fn)
            return fn

        return decorator

    def _get_payload(self, token: str):
        """
        Returns the decoded token payload
        Args:
            token: The token to decode
        Returns:
            Payload of the token
        Raises:
            LoginManager.not_authenticated_exception: The token is invalid or None was returned by `_load_user`
        """
        try:
            payload = jwt.decode(
                token, self.secret.secret_for_decode, algorithms=[self.algorithm]
                # token, "secret", algorithms=[self.algorithm]
            )
            return payload
        # This includes all errors raised by pyjwt
        except jwt.PyJWTError as e:
            raise self.not_authenticated_exception

    async def get_current_user(self, token: str):
        """
        This decodes the jwt based on the secret and the algorithm set on the instance.
        If the token is correctly formatted and the user is found the user object
        is returned else this raises `LoginManager.not_authenticated_exception`
        Args:
            token (str): The encoded jwt token
        Returns:
            The user object returned by the instances `_user_callback`
        Raises:
            LoginManager.not_authenticated_exception: The token is invalid or None was returned by `_load_user`
        """
        payload = self._get_payload(token)

        # the identifier should be stored under the sub (subject) key
        user_identifier = payload.get("sub")
        if user_identifier is None:
            raise self.not_authenticated_exception
        user = await self._load_user(user_identifier)
        if user is None:
            raise self.not_authenticated_exception
        return user

    async def _load_user(self, identifier: typing.Any):
        """
        This loads the user using the user_callback
        Args:
            identifier (Any): The user identifier expected by `_user_callback`
        Returns:
            The user object returned by `_user_callback` or None
        Raises:
            Exception: When no ``user_loader`` has been set
        """
        if self._user_callback is None:
            raise Exception("Missing user_loader callback")
        if inspect.iscoroutinefunction(self._user_callback):
            user = await self._user_callback(identifier)
        else:
            user = self._user_callback(identifier)
        return user

    def create_access_token(
        self, *, data: dict, expires: timedelta = None, scopes: Collection[str] = None
    ) -> str:
        """
        Helper function to create the encoded access token using
        the provided secret and the algorithm of the LoginManager instance
        Args:
            data (dict): The data which should be stored in the token
            expires (datetime.timedelta):  An optional timedelta in which the token expires.
                Defaults to 15 minutes
            scopes (Collection): Optional scopes the token user has access to.
        Returns:
            The encoded JWT with the data and the expiry. The expiry is
            available under the 'exp' key
        """

        to_encode = data.copy()

        if expires:
            expires_in = datetime.utcnow() + expires
        else:
            expires_in = datetime.utcnow() + self.default_expiry

        to_encode.update({"exp": expires_in})

        if scopes is not None:
            unique_scopes = set(scopes)
            to_encode.update({"scopes": list(unique_scopes)})

        encoded_jwt = jwt.encode(
            to_encode, self.secret.secret_for_encode, self.algorithm
            # to_encode, "secret", self.algorithm
        )
        return encoded_jwt

    def set_cookie(self, response: Response, token: str) -> None:
        """
        Utility function to set a cookie containing token on the response
        Args:
            response (fastapi.Response): The response which is send back
            token (str): The created JWT
        """
        response.set_cookie(key=self.cookie_name, value=token, httponly=True, max_age=60*60*24*7)

    def _token_from_cookie(self, request: Request) -> typing.Optional[str]:
        """
        Checks the requests cookies for cookies with the value of`self.cookie_name` as name
        Args:
            request (fastapi.Request):  The request to the route, normally filled in automatically
        Returns:
            The access token found in the cookies of the request or None
        Raises:
            LoginManager.not_authenticated_exception: When no cookie with name ``LoginManager.cookie_name``
                is set on the Request
        """
        token = request.cookies.get(self.cookie_name)

        # we don't use `token is None` in case a cookie with self.cookie_name
        # exists but is set to "", in which case `token is None` evaluates to False
        if not token and self.auto_error:
            # either default InvalidCredentialsException or set by user
            raise self.not_authenticated_exception

        else:
            return token if token else None

    async def _get_token(self, request: Request):
        token = None
        try:
            token = self._token_from_cookie(request)
        except Exception as _e:
            raise self.not_authenticated_exception
        return token

    async def __call__(self, request: Request, security_scopes: SecurityScopes = None):
        """
        Provides the functionality to act as a Dependency
        Args:
            request (fastapi.Request):The incoming request, this is set automatically
                by FastAPI
        Returns:
            The user object or None
        Raises:
            LoginManager.not_authenticated_exception: If set by the user and `self.auto_error` is set to False
        """

        token = await self._get_token(request)

        if token is None:
            raise self.not_authenticated_exception
        return await self.get_current_user(token)

    def useRequest(self, app: FastAPI):
        """
        Add the instance as a middleware, which adds the user object, if present,
        to the request state
        Args:
            app (fastapi.FastAPI): A instance of FastAPI
        """

        @app.middleware("http")
        async def user_middleware(request: Request, call_next):
            try:
                request.state.user = self.__call__(request)
            except Exception as _e:
                request.state.user = None
            return await call_next(request)
