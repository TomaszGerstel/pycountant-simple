import datetime
from dataclasses import dataclass
from typing import Optional

from enum import Enum


class Client(Enum):
    MCDONALDS = "McDonald's"


@dataclass
class Invoice:
    amount: float
    client: str
    worker: str
    date: datetime = datetime.date.today()
    descr: str = ""


@dataclass
class Transfer:
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


def sum_transfers(tr_arr):
    _sum = 0
    for t in tr_arr:
        _sum += t.amount
    return _sum


def sum_transfers_generator(tr_arr):
    return sum(t.amount for t in tr_arr)


def main():

    inv1 = Invoice(amount=500.00, client="Burger King", worker="me", descr="data analysis")
    print(inv1)

    t2 = Transfer(invoice=inv1, amount=500.00, _from="Burger Queen", _to="me", descr="data analysis")
    print(t2)
    t3 = Transfer(amount=1500.00, _from="Burger King", _to="me", descr="gift")

    tr_arr = [t2, t3]
    print(tr_arr)

    s = sum_transfers(tr_arr)
    print(s)

    s = sum_transfers_generator(tr_arr)
    print(s)


if __name__ == "__main__":
    main()