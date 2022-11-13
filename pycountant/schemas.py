from enum import Enum

from pydantic import BaseModel
from typing import Optional, Sequence, Any
from pydantic.schema import date, datetime

from pycountant.config import config


class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferType(str, Enum):
    IN_TRANSFER = "InTransfer"
    OUT_TRANSFER = "OutTransfer"
    VAT_OUT_TRANSFER = "VatOutTransfer"
    TAX_OUT_TRANSFER = "TaxOutTransfer"
    SALARY = "Salary"


class UserSearch(BaseModel):
    id: int
    name: str
    password: str
    email: str


class UserCreate(BaseModel):
    name: str
    password: str
    email: str


class ReceiptSearch(BaseModel):
    id: int
    amount: float
    client: str
    worker: str
    date: date
    user_id: Optional[int] = None
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    descr: str = ""

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.net_amount is None and self.vat_value is None:
            self.net_amount = (self.amount / (100 + self.vat_percentage) * 100).__round__(2)
            self.vat_value = (self.amount - self.net_amount).__round__(2)
        elif self.net_amount is None:
            self.net_amount = (self.amount - self.vat_value).__round__(2)
        elif self.vat_value is None:
            self.vat_value = (self.amount - self.net_amount).__round__(2)

    def __repr__(self):
        return (
            f"Receipt with id: {self.id} date: {self.date} from: {self.worker} to: {self.client} with amount: {self.amount} "
            f"with vat: {self.vat_value} net amount: {self.net_amount} vat percentage: {self.vat_percentage} "
            f"for: {self.descr}"
        )


# not used
class ReceiptSearchResults(BaseModel):
    results: Sequence[ReceiptSearch]


class ReceiptCreate(BaseModel):
    amount: float
    client: str
    worker: str
    user_id: int
    date: date
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    descr: str = ""


class TransferSearch(BaseModel):
    id: int
    transfer_type: TransferType
    amount: Optional[float]
    receipt_id: Optional[int]
    user_id: Optional[int] = None
    from_: Optional[str]
    to_: Optional[str]
    date: Optional[date]
    base_date: Optional[datetime]
    descr: Optional[str]


class TransferSearchResults(BaseModel):
    results: Sequence[TransferSearch]


class TransferCreate(BaseModel):
    transfer_type: TransferType
    amount: float
    user_id: Optional[int] = None
    receipt_id: Optional[int] = None
    from_: Optional[str] = None
    to_: Optional[str] = None
    base_date: Optional[datetime]
    date: Optional[date]
    descr: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.base_date = datetime.today().replace(microsecond=0)
        if self.date is None:
            self.date = datetime.date(self.base_date)


# used in calculations
class TransactionToCalculate(BaseModel):
    transfer_type: TransferType
    amount: float
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percentage: Optional[float] = 0
    tax_percentage: float = config.income_flat_tax_pct
