from pydantic import BaseModel
from typing import Optional, Sequence
import datetime

from pycountant.model import TransferType
from pycountant.config import config


class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferType(Enum):
    IN_TRANSFER = "InTransfer"
    OUT_TRANSFER = "OutTransfer"


class Receipt(BaseModel):
    id: int
    amount: float
    client: str
    worker: str
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    # tax_percentage can be deleted? method get_calc_income_tax_30 returns 30% tax
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date as a optional value? if None: get present date?
    # date: datetime = datetime.date.today()

    def __post_init__(self):
        if self.net_amount is None and self.vat_value is None:
            self.net_amount = self.amount / (100 + self.vat_percent) * 100
            self.vat_value = self.amount - self.net_amount
        elif self.net_amount is None:
            self.net_amount = self.amount - self.vat_value
        elif self.vat_value is None:
            self.vat_value = self.amount - self.net_amount


class ReceiptSearchResults(BaseModel):
    results: Sequence[Receipt]


class ReceiptCreate(BaseModel):
    amount: float
    client: str
    worker: str
    submitter_id: int
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date: datetime = datetime.date.today()


class Transfer(BaseModel):
    id: int
    transfer_type: TransferType
    amount: Optional[float] = None
    # receipt_id: Optional[int] = None
    receipt: Receipt = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""

    def __post_init__(self):
        if self.receipt is not None:
            if not self._from:
                self._from = self.receipt.client
            if not self._to:
                self._to = self.receipt.worker
            if not self.amount:
                self.amount = self.receipt.amount
            if self.descr == "":
                self.descr = self.receipt.descr


class TransferSearchResults(BaseModel):
    results: Sequence[Transfer]


class TransferCreate(BaseModel):
    transfer_type: TransferType
    amount: float
    submitter_id: int
    receipt_id: Optional[int] = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""
