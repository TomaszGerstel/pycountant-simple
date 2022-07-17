from pydantic import BaseModel
from typing import Optional, Sequence
import datetime

from pycountant.model import TransferType
from pycountant.config import config


class Invoice(BaseModel):
    id: int
    amount: float
    client: str
    worker: str
    vat_percentage: float = config.vat_pct
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date: datetime = datetime.date.today()  # zmienic


class InvoiceSearchResults(BaseModel):
    results: Sequence[Invoice]


class InvoiceCreate(BaseModel):
    amount: float
    client: str
    worker: str
    submitter_id: int
    vat_percentage: float = config.vat_pct
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date: datetime = datetime.date.today()  # zmienic


class Transfer(BaseModel):
    id: int
    transfer_type: TransferType
    amount: float
    invoice_id: Optional[int] = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""


class TransferSearchResults(BaseModel):
    results: Sequence[Transfer]


class TransferCreate(BaseModel):
    transfer_type: TransferType
    amount: float
    submitter_id: int
    invoice_id: Optional[int] = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""
