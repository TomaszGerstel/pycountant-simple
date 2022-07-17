import datetime
from abc import ABC
from dataclasses import dataclass
from pydantic import BaseModel

from enum import Enum
from typing import Optional

from pycountant.config import config


class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferType(Enum):
    IN_TRANSFER = "InTransfer"
    OUT_TRANSFER = "OutTransfer"


class AnyInvoice(BaseModel):
    amount: float
    client: str
    worker: str
    vat_percentage: float = config.vat_pct
    tax_percentage: float = config.income_tax_pct
    descr: str = ""
    #date: datetime = datetime.date.today()  # zmienic


class AnyTransfer(BaseModel):
    transfer_type: TransferType
    amount: float
    invoice_id: Optional[int] = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""



class Invoice(ABC):
    amount: float
    net_amount: float
    vat_percent: float
    vat_value: float
    client: str
    worker: str
    descr: str = ""
    date: datetime = datetime.date.today()  # zmienic

    def __init__(self, amount, client, worker, descr):
        self.amount = amount
        self.client = client
        self.worker = worker
        self.descr = descr

    def __set_net_amount_and_vat(self):
        raise NotImplementedError


class DefaultVatInvoice(Invoice):
    def __init__(self, amount, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.vat_percent = config.vat_pct
        self.net_amount = self.amount / (100 + config.vat_pct) * 100
        self.vat_value = self.amount - self.net_amount


class NoVatInvoice(Invoice):
    def __init__(self, amount, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.vat_percent = 0
        self.vat_value = 0
        self.net_amount = self.amount


class FixedVatInvoice(Invoice):
    def __init__(self, amount, vat_percent, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.vat_percent = vat_percent
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.net_amount = self.amount / (100 + self.vat_percent) * 100
        self.vat_value = self.amount - self.net_amount


@dataclass
class Transfer:
    transfer_type: TransferType
    invoice: Invoice = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    amount: Optional[float] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""

    def __post_init__(self):
        if self.invoice is not None:
            if not self._from:
                self._from = self.invoice.client
            if not self._to:
                self._to = self.invoice.worker
            if not self.amount:
                self.amount = self.invoice.amount
            if self.descr == "":
                self.descr = self.invoice.descr
