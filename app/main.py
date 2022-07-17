from fastapi import FastAPI, APIRouter, HTTPException
from typing import Optional

from pycountant.sample_data import INVOICES_ANY, TRANSFERS_ANY
from pycountant.schemas import (
    Invoice,
    InvoiceCreate,
    InvoiceSearchResults,
    Transfer,
    TransferCreate,
    TransferSearchResults,
)


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/invoice/{invoice_id}", status_code=200, response_model=Invoice)
def fetch_invoice(*, invoice_id: int) -> dict:
    """
    Fetch a single invoice by ID
    """

    result = [invoice for invoice in INVOICES_ANY if invoice["id"] == invoice_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {invoice_id} not found"
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
    "/search/invoice/", status_code=200, response_model=InvoiceSearchResults
)
def search_invoices(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """
    Search for invoices based on label keyword

    Enables eg:
    http://0.0.0.0:8001/search/invoice/?keyword=burger king
    (browser replaces ' ' with %20)
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": INVOICES_ANY[:max_results]}

    results = filter(
        lambda invoice: keyword.lower() in invoice["client"].lower(), INVOICES_ANY
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
@api_router.post("/invoice/", status_code=201, response_model=Invoice)
def create_invoice(*, invoice_in: InvoiceCreate) -> dict:
    """
    Create a new invoice (in memory only)
    """
    new_entry_id = len(INVOICES_ANY) + 1
    invoice_entry = Invoice(
        id=new_entry_id,
        amount=invoice_in.amount,
        client=invoice_in.client,
        worker=invoice_in.worker,
        vat_percentage=invoice_in.vat_percentage,
        tax_percentage=invoice_in.tax_percentage,
        descr=invoice_in.descr,
    )
    INVOICES_ANY.append(invoice_entry.dict())

    return invoice_entry


@api_router.post("/transfer/", status_code=201, response_model=Transfer)
def create_invoice(*, transfer_in: TransferCreate) -> dict:
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
