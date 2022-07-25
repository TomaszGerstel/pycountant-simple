from enum import Enum

from pydantic import BaseModel
from typing import Optional, Sequence, Any
import datetime

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
    vat_value: Optional[float] = 0
    net_amount: Optional[float] = 0
    vat_percentage: Optional[float] = 0
    # tax_percentage can be deleted? method get_calc_income_tax_30 returns 30% tax
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date as a optional value? if None: get present date?
    # date: datetime = datetime.date.today()

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.net_amount == 0 and self.vat_value == 0:
            self.net_amount = self.amount / (100 + self.vat_percentage) * 100
            self.vat_value = self.amount - self.net_amount
        elif self.net_amount == 0:
            self.net_amount = self.amount - self.vat_value
        elif self.vat_value == 0:
            self.vat_value = self.amount - self.net_amount


class ReceiptSearchResults(BaseModel):
    results: Sequence[Receipt]


class ReceiptCreate(BaseModel):
    amount: float
    client: str
    worker: str
    submitter_id: int
    vat_value: Optional[float] = 0
    net_amount: Optional[float] = 0
    vat_percentage: Optional[float] = 0
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date: datetime = datetime.date.today()


class Transfer(BaseModel):
    id: int
    transfer_type: TransferType
    amount: Optional[float]
    # receipt_id: Optional[int] = None
    receipt: Receipt
    from_: Optional[str]
    to_: Optional[str]
    date: datetime.datetime = datetime.date.today()
    descr: str = ""

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.receipt is not None:
            if not self.from_:
                self.from_ = self.receipt.client
            if not self.to_:
                self.to_ = self.receipt.worker
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
    receipt_id: Optional[int]
    from_: Optional[str]
    to_: Optional[str]
    date: datetime.datetime = datetime.date.today()
    descr: str = ""
