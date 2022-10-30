import datetime
from datetime import date

from fastapi import FastAPI, APIRouter, HTTPException, Request, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from pathlib import Path
from app.api.deps import manager
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.templating import _TemplateResponse

from db import crud_transfer, crud_receipt, crud_user
from fastapi_login.exceptions import InvalidCredentialsException, InvalidRegistrationException
from pycountant import calculations
from pycountant.schemas import (
    ReceiptSearch,
    ReceiptCreate,
    ReceiptSearchResults,
    TransferSearch,
    TransferCreate,
    TransferSearchResults, UserCreate,
)
from pycountant.model import Transfer
from pycountant.calculations import BalanceResults
from app.api import deps
from db.session import Session

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")
api_router = APIRouter()
session = Session()


@api_router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = deps.load_user(username=username)
    if not user:
        raise InvalidCredentialsException  # return info instead exception?
    elif password != user.password:
        raise InvalidCredentialsException
    access_token = deps.manager.create_access_token(
        data={"sub": username}
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    deps.manager.set_cookie(response, access_token)
    deps.manager.user_name = username
    deps.manager.current_user_id = user.id
    deps.current_user_id = user.id
    return response


@api_router.post("/register")
def register(request: Request, name: str = Form(), password: str = Form(),
             conf_password: str = Form(), email: str = Form()):
    if password != conf_password:
        raise InvalidRegistrationException(detail="passwords are different")
    if crud_user.get(name=name, session=session) is not None:
        raise InvalidRegistrationException(detail=f"user with this name ({name}) already exists")

    new_user = UserCreate(
        name=name,
        password=password,
        email=email,
    )

    user = crud_user.create(user_create=new_user, session=session)
    user_name = user.name
    info = f"you are registered, {user_name}, now log in:"

    return TEMPLATES.TemplateResponse(
        "login.html", {"request": request, "login_info": info})


@api_router.get("/register", status_code=200)
def register_form(request: Request) -> _TemplateResponse:
    """
    register form
    """
    return TEMPLATES.TemplateResponse(
        "register.html", {"request": request}
    )


@api_router.get("/login", status_code=200)
def login_form(request: Request) -> _TemplateResponse:
    """
    login form
    """
    return TEMPLATES.TemplateResponse(
        "login.html", {"request": request}
    )


@api_router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=deps.manager.cookie_name)
    return response


@api_router.get("/", status_code=200)
def root(
        request: Request,
        _=Depends(deps.manager),
        transfers: List[Transfer] = Depends(deps.get_transfers),
        balance: BalanceResults = Depends(deps.get_balance),
) -> _TemplateResponse:
    """
    Root GET
    """
    current_user = deps.manager.user_name
    if request.cookies.get(deps.manager.cookie_name) is None:
        return TEMPLATES.TemplateResponse("login.html", {"request": request})
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "transfers": transfers, "balance": balance, "user": current_user},
    )


@api_router.post("/balance", status_code=200)
def get_balance(*, _=Depends(deps.manager), from_date: date = Form(), to_date: date = Form(), request: Request,
                current_balance: BalanceResults = Depends(deps.get_balance)) -> _TemplateResponse:

    balance = calculations.balance_to_date_range(session=session, user_id=manager.current_user_id,
                                                 from_date=from_date, to_date=to_date)
    return TEMPLATES.TemplateResponse(
        "balance_result.html",
        {"request": request, "balance": balance, "current_balance": current_balance,
         "from_date": from_date, "to_date": to_date}
    )


# New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/receipt/{receipt_id}", status_code=200, response_model=ReceiptSearch)
def fetch_receipt(*, _=Depends(deps.manager), receipt_id: int, request: Request) -> _TemplateResponse:
    """
    Fetch a single receipt by ID
    """
    result = crud_receipt.get(receipt_id, session)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Receipt with ID {receipt_id} not found"
        )
    return TEMPLATES.TemplateResponse(
        "receipt.html", {"request": request, "receipt": result}
    )


@api_router.get(
    "/transfer/{transfer_id}", status_code=200, response_model=TransferSearch
)
def fetch_transfer(*, _=Depends(deps.manager), transfer_id: int, request: Request) -> _TemplateResponse:
    """
    Fetch a single transfer by ID
    """
    transfer = crud_transfer.get(session=session, id=transfer_id)
    if not transfer:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Transfer with ID {transfer_id} not found"
        )
    return TEMPLATES.TemplateResponse(
        "transfer.html", {"request": request, "transfer": transfer}
    )


@api_router.get("/search", status_code=200)
def search_form(request: Request) -> _TemplateResponse:
    """
    login form
    """
    return TEMPLATES.TemplateResponse(
        "search.html", {"request": request}
    )


# New addition, query parameter
# https://fastapi.tiangolo.com/tutorial/query-params/
@api_router.get("/search/receipt/", status_code=200, response_model=ReceiptSearchResults)
def search_receipts(
        request: Request,
        _=Depends(deps.manager),
        keyword: Optional[str] = None, max_results: Optional[int] = 10,
        receipts: List[ReceiptSearch] = Depends(deps.get_receipts)
) -> _TemplateResponse:
    """
    Search for receipts based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/receipt/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    results = []
    if not keyword:
        results = receipts[:max_results]
    if keyword:
        results = list(filter(
            lambda receipt: receipt.client is not None
                            and keyword.lower() in receipt.client.lower(), receipts
        ))

    return TEMPLATES.TemplateResponse(
        "search_receipts_result.html",
        {"request": request, "results": results},
    )


@api_router.get("/search/transfer/", status_code=200, response_model=TransferSearchResults)
def search_transfers(
        request: Request,
        _=Depends(deps.manager),
        keyword: Optional[str] = None, max_results: Optional[int] = 10,
        transfers: List[TransferSearch] = Depends(deps.get_transfers)
) -> _TemplateResponse:
    """
    Search for transfers based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/transfer/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    results = []
    if not keyword:
        results = transfers[:max_results]
    if keyword:
        results = list(filter(
            lambda transfer: transfer.from_ is not None
                             and keyword.lower() in transfer.from_.lower(), transfers
        ))
    return TEMPLATES.TemplateResponse(
        "search_transfers_result.html",
        {"request": request, "results": results},
    )


@api_router.get("/create_receipt/", status_code=200)
def receipt_form(request: Request) -> _TemplateResponse:
    """
    receipt form
    """
    auth_info = ""
    if request.cookies.get(deps.manager.cookie_name) is None:
        auth_info = "You're not logged in. You cannot submit the form!"
    return TEMPLATES.TemplateResponse(
        "create_receipt.html",
        {"request": request, "auth_info": auth_info},
    )


# New addition, using Pydantic model `InvoiceCreate` to define
# the POST request body
@api_router.post("/receipt/", status_code=201, response_model=ReceiptCreate)
def create_receipt(
        _=Depends(deps.manager),
        amount: float = Form(),
        client: str = Form(),
        worker: str = Form(),
        date: date = Form(),
        vat_value: float = Form(default=None),
        net_amount: float = Form(default=None),
        vat_percentage: float = Form(default=0),
        descr: str = Form(),
):
    """
    Create a new receipt in the database
    """
    receipt_in = ReceiptCreate(
        date=date,
        amount=amount,
        client=client,
        worker=worker,
        vat_value=vat_value,
        net_amount=net_amount,
        vat_percentage=vat_percentage,
        descr=descr,
        user_id=deps.manager.current_user_id
    )
    receipt = crud_receipt.create(receipt_in, session)
    rec_id = receipt.id

    # return receipt
    return RedirectResponse(url=f"/receipt/{rec_id}", status_code=302)


@api_router.get("/create_transfer/", status_code=201, response_model=TransferCreate)
def transfer_form(request: Request,
                  receipts: List[ReceiptSearch] = Depends(deps.get_receipts_without_transfer),
                  balance: BalanceResults = Depends(deps.get_balance)
                  ) -> _TemplateResponse:
    """
    transfer form with available receipts
    """
    auth_info = ""
    if request.cookies.get(deps.manager.cookie_name) is None:
        auth_info = "You're not logged in. You cannot submit the form!"
    # receipts = crud_receipt.get_all_without_transfer(session)
    return TEMPLATES.TemplateResponse(
        "create_transfer.html",
        {"request": request, "receipts": receipts, "auth_info": auth_info, "balance": balance},
    )


@api_router.post("/transfer/", status_code=201, response_model=TransferCreate)
def create_transfer(
        _=Depends(deps.manager),
        transfer_type: str = Form(),
        amount: float = Form(),
        receipt_id: int = Form(default=None),
        from_: str = Form(default=None),
        to_: str = Form(default=None),
        descr: str = Form(default=None),
) -> RedirectResponse:
    """
    Create a new transfer
    """
    transfer_in = TransferCreate(
        transfer_type=transfer_type,
        amount=amount,
        receipt_id=receipt_id,
        from_=from_,
        to_=to_,
        descr=descr,
        user_id=deps.manager.current_user_id
    )
    transfer = crud_transfer.create(transfer_in, session)
    tr_id = transfer.id

    # return transfer
    return RedirectResponse(url=f"/transfer/{tr_id}", status_code=302)


@api_router.post("/delete/transfer/", status_code=202)
def delete_transfer(_=Depends(deps.manager), transfer_id: int = Form()):
    crud_transfer.delete(tr_id=transfer_id, session=session)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response


@api_router.post("/delete/receipt/", status_code=202)
def delete_receipt(_=Depends(deps.manager), receipt_id: int = Form()):
    crud_receipt.delete(rec_id=receipt_id, session=session)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response


@app.exception_handler(InvalidCredentialsException)
async def myCustomExceptionHandler(request: Request, exception: InvalidCredentialsException):
    info = "Invalid credentials!"
    return TEMPLATES.TemplateResponse(
        "login.html", {"request": request, "login_info": info}, status_code=HTTP_401_UNAUTHORIZED
    )


@app.exception_handler(InvalidRegistrationException)
async def myCustomExceptionHandler(request: Request, exception: InvalidRegistrationException):
    info = exception.detail

    return TEMPLATES.TemplateResponse(
        "register.html", {"request": request, "register_info": info}, status_code=HTTP_401_UNAUTHORIZED
    )


app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
