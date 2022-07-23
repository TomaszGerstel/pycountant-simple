from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path

from pycountant.sample_data import RECEIPTS_ANY, TRANSFERS_ANY
from pycountant.schemas import (
    Receipt,
    ReceiptCreate,
    ReceiptSearchResults,
    Transfer,
    TransferCreate,
    TransferSearchResults,
)


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "transfers": TRANSFERS_ANY},
    )


# New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/receipt/{receipt_id}", status_code=200, response_model=Receipt)
def fetch_receipt(*, receipt_id: int) -> dict:
    """
    Fetch a single receipt by ID
    """

    result = [receipt for receipt in RECEIPTS_ANY if receipt["id"] == receipt_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {receipt_id} not found"
        )
    return result[0]


@api_router.get("/transfer/{transfer_id}", status_code=200, response_model=Transfer)
def fetch_transfer(*, transfer_id: int) -> dict:
    """
    Fetch a single transfer by ID
    """

    result = [transfer for transfer in TRANSFERS_ANY if transfer["id"] == transfer_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Transfer with ID {transfer_id} not found"
        )
    return result[0]


# New addition, query parameter
# https://fastapi.tiangolo.com/tutorial/query-params/
@api_router.get(
    "/search/invoice/", status_code=200, response_model=ReceiptSearchResults
)
def search_receipts(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """
    Search for invoices based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/receipt/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECEIPTS_ANY[:max_results]}

    results = filter(
        lambda invoice: keyword.lower() in invoice["client"].lower(), RECEIPTS_ANY
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
        lambda transfer: keyword.lower() in transfer["_from"].lower(), TRANSFERS_ANY
    )
    return {"results": list(results)[:max_results]}


# New addition, using Pydantic model `InvoiceCreate` to define
# the POST request body
@api_router.post("/invoice/", status_code=201, response_model=Receipt)
def create_receipt(*, invoice_in: ReceiptCreate) -> dict:
    """
    Create a new invoice (in memory only)
    """
    new_entry_id = len(RECEIPTS_ANY) + 1
    receipt_entry = Receipt(
        id=new_entry_id,
        amount=invoice_in.amount,
        client=invoice_in.client,
        worker=invoice_in.worker,
        vat_percentage=invoice_in.vat_percentage,
        tax_percentage=invoice_in.tax_percentage,
        descr=invoice_in.descr,
    )
    RECEIPTS_ANY.append(receipt_entry.dict())

    return receipt_entry


@api_router.post("/transfer/", status_code=201, response_model=Transfer)
def create_transfer(*, transfer_in: TransferCreate) -> dict:
    """
    Create a new transfer (in memory only)
    """
    new_entry_id = len(TRANSFERS_ANY) + 1
    transfer_entry = Transfer(
        id=new_entry_id,
        transfer_type=transfer_in.transfer_type,
        amount=transfer_in.amount,
        _from=transfer_in._from,
        _to=transfer_in._to,
        date=transfer_in.date,
        descr=transfer_in.descr,
    )
    TRANSFERS_ANY.append(transfer_entry.dict())

    return transfer_entry


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
