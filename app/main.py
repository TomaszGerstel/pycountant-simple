from fastapi import FastAPI, APIRouter, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from pathlib import Path

from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from db import crud_transfer, crud_receipt

from pycountant.sample_data import RECEIPTS_ANY, TRANSFERS_ANY
from pycountant.schemas import (
    ReceiptSearch,
    ReceiptCreate,
    ReceiptSearchResults,
    TransferSearch,
    TransferCreate,
    TransferSearchResults,
)
from pycountant.model import Transfer
from pycountant.calculations import BalanceResults
from app.api import deps

from db.session import Session

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")
api_router = APIRouter()

session = Session()


@api_router.get("/", status_code=200)
def root(
    request: Request,
    transfers: List[Transfer] = Depends(deps.get_transfers),
    balance: BalanceResults = Depends(deps.get_balance),
) -> _TemplateResponse:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "transfers": transfers, "balance": balance},
    )


# New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/receipt/{receipt_id}", status_code=200, response_model=ReceiptSearch)
def fetch_receipt(*, receipt_id: int, request: Request) -> _TemplateResponse:
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
def fetch_transfer(*, transfer_id: int, request: Request) -> _TemplateResponse:
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


# New addition, query parameter
# https://fastapi.tiangolo.com/tutorial/query-params/
@api_router.get(
    "/search/receipt/", status_code=200, response_model=ReceiptSearchResults
)
def search_receipts(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """
    Search for receipts based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/receipt/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECEIPTS_ANY[:max_results]}

    results = filter(
        lambda receipt: keyword.lower() in receipt["client"].lower(), RECEIPTS_ANY
    )
    return {"results": list(results)[:max_results]}


@api_router.get(
    "/search/transfer/", status_code=200, response_model=TransferSearchResults
)
def search_transfers(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """
    Search for transfers based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/transfer/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": TRANSFERS_ANY[:max_results]}

    results = filter(
        lambda transfer: keyword.lower() in transfer["from_"].lower(), TRANSFERS_ANY
    )
    return {"results": list(results)[:max_results]}


@api_router.get("/create_receipt/", status_code=200)
def receipt_form(request: Request) -> _TemplateResponse:
    """
    receipt form
    """
    return TEMPLATES.TemplateResponse(
        "create_receipt.html",
        {"request": request},
    )


# New addition, using Pydantic model `InvoiceCreate` to define
# the POST request body
@api_router.post("/receipt/", status_code=201, response_model=ReceiptCreate)
def create_receipt(
    amount: float = Form(),
    client: str = Form(),
    worker: str = Form(),
    vat_value: float = Form(default=None),
    net_amount: float = Form(default=None),
    vat_percentage: float = Form(default=0),
    descr: str = Form(),
):
    """
    Create a new receipt in the database
    """
    receipt_in = ReceiptCreate(
        amount=amount,
        client=client,
        worker=worker,
        vat_value=vat_value,
        net_amount=net_amount,
        vat_percentage=vat_percentage,
        descr=descr,
    )
    receipt = crud_receipt.create(receipt_in, session)
    rec_id = receipt.id

    # return receipt
    return RedirectResponse(url=f"/receipt/{rec_id}", status_code=302)


@api_router.get("/create_transfer/", status_code=201, response_model=TransferCreate)
def transfer_form(request: Request) -> _TemplateResponse:
    """
    transfer form with available receipts
    """
    receipts = crud_receipt.get_all_without_transfer(session)
    return TEMPLATES.TemplateResponse(
        "create_transfer.html",
        {"request": request, "receipts": receipts},
    )


@api_router.post("/transfer/", status_code=201, response_model=TransferCreate)
def create_transfer(
    transfer_type: str = Form(),
    amount: float = Form(),
    receipt_id: int = Form(),
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
    )
    transfer = crud_transfer.create(transfer_in, session)
    tr_id = transfer.id

    # return transfer
    return RedirectResponse(url=f"/transfer/{tr_id}", status_code=302)


app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
