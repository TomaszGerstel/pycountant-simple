import datetime
from abc import ABC
from dataclasses import dataclass

from enum import Enum
from typing import Optional


class Client(Enum):
    MCDONALDS = "McDonald's"

class TransferType(Enum):
    IN_TRANSFER = "InTransfer"
    OUT_TRANSFER = "OutTransfer"


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

    # @abstractmethod
    def __set_net_amount_and_vat(self):
        pass


class DefaultVatInvoice(Invoice):

    def __init__(self, amount, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.vat_percent = 30
        self.net_amount = self.amount / (100 + 30) * 100
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