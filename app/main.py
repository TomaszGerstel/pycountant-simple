from fastapi import FastAPI, APIRouter

from pycountant.sample_data import INVOICES_ANY, TRANSFERS_ANY


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
@api_router.get("/invoice/{invoice_id}", status_code=200)
def fetch_invoice(*, invoice_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """

    result = [invoice for invoice in INVOICES_ANY if invoice["id"] == invoice_id]
    if result:
        return result[0]


@api_router.get("/transfer/{transfer_id}", status_code=200)
def fetch_transfer(*, transfer_id: int) -> dict:
    """
    Fetch a single transfer by ID
    """

    result = [transfer for transfer in TRANSFERS_ANY if transfer["id"] == transfer_id]
    if result:
        return result[0]


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")