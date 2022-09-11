from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


# InvalidCredentialsException = HTTPException(
#     status_code=HTTP_401_UNAUTHORIZED,
#     detail="Invalid credentials",
#     headers={"WWW-Authenticate": "Bearer"}
# )

class InvalidCredentialsException(Exception):
    # def __init__(self, name: str):
    #     self.name = name
    pass
