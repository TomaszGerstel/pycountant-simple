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


@dataclass
class Receipt:
    amount: float
    client: str
    worker: str
    descr: str = ""
    date: datetime = datetime.date.today()
    vat_value: Optional[float] = None
    net_amount: Optional[float] = None
    vat_percent: Optional[float] = 0

    def __post_init__(self):
        if self.net_amount is None and self.vat_value is None:
            self.net_amount = self.amount / (100 + self.vat_percent) * 100
            self.vat_value = self.amount - self.net_amount
        elif self.net_amount is None:
            self.net_amount = self.amount - self.vat_value
        elif self.vat_value is None:
            self.vat_value = self.amount - self.net_amount


@dataclass
class Transfer:
    transfer_type: TransferType
    receipt: Receipt = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    amount: Optional[float] = None
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
