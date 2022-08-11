from enum import Enum

from pydantic import BaseModel
from typing import Optional, Sequence, Any
import datetime

from db import crud_receipt
from pycountant.config import config
from db.session import Session

session = Session()

class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferType(str, Enum):
    IN_TRANSFER = "InTransfer"
    OUT_TRANSFER = "OutTransfer"


class ReceiptSearch(BaseModel):
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

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.net_amount is None and self.vat_value is None:
            self.net_amount = self.amount / (100 + self.vat_percentage) * 100
            self.vat_value = self.amount - self.net_amount
        elif self.net_amount is None:
            self.net_amount = self.amount - self.vat_value
        elif self.vat_value is None:
            self.vat_value = self.amount - self.net_amount


# not used
class ReceiptSearchResults(BaseModel):
    results: Sequence[ReceiptSearch]


class ReceiptCreate(BaseModel):
    amount: float
    client: str
    worker: str
    # submitter_id: int
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    # tax_percentage: float = config.income_tax_pct
    descr: str = ""
    # date: datetime = datetime.date.today()


class TransferSearch(BaseModel):
    id: int
    transfer_type: TransferType
    amount: Optional[float]
    # receipt: ReceiptSearch = None
    receipt_id: int
    from_: Optional[str]
    to_: Optional[str]
    date: Optional[datetime.date]
    descr: Optional[str]

    # def __init__(self, **data: Any):
    #     super().__init__(**data)
    #     # copies uncompleted data from receipt
    #     receipt = crud_receipt.get(self.receipt_id, session)
    #     if not self.from_:
    #         self.from_ = receipt.client
    #     if not self.to_:
    #         self.to_ = receipt.worker
    #     if not self.amount:
    #         self.amount = receipt.amount
    #     if not self.descr:
    #         self.descr = receipt.descr


class TransferSearchResults(BaseModel):
    results: Sequence[TransferSearch]


class TransferCreate(BaseModel):
    transfer_type: TransferType
    amount: float
    # submitter_id: int
    receipt_id: int
    from_: Optional[str] = None
    to_: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: Optional[str] = None


# used in calculations
class TransactionToCalculate(BaseModel):
    transfer_type: TransferType
    amount: float
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    tax_percentage: float = config.income_tax_pct
