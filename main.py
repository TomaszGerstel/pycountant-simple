import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from enum import Enum

from exceptions import NegativeValueError


class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferType(Enum):
    IN_TRANSFER = "Incoming transfer"
    OUT_TRANSFER = "Outgoing transfer"


class Invoice(ABC):
    amount: float
    net_amount: float
    vat_per_cent: float
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

    # def __post_init__(self):
    #     self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.vat_per_cent = 30
        self.net_amount = self.amount / (100 + 30) * 100
        self.vat_value = self.amount - self.net_amount


class NoVatInvoice(Invoice):

    def __init__(self, amount, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.vat_per_cent = 0
        self.vat_value = 0
        self.net_amount = self.amount


class FixedVatInvoice(Invoice):

    def __init__(self, amount, vat_per_cent, client, worker, descr):
        super().__init__(amount, client, worker, descr)
        self.vat_per_cent = vat_per_cent
        self.__set_net_amount_and_vat()

    def __set_net_amount_and_vat(self):
        self.net_amount = self.amount / (100 + self.vat_per_cent) * 100
        self.vat_value = self.amount - self.net_amount


@dataclass
class Transfer:
    transfer_type: TransferType
    invoice: Invoice = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    amount: Optional[float] = None
    # net_amount: Optional[float] = None
    # vat_per_cent: Optional[float] = None
    # vat_value: Optional[float] = None
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
        if t.amount <= 0:
            raise NegativeValueError('amount can\'t be negative value')
        _sum += t.amount
    return _sum


def sum_transfers_generator(tr_arr):
    return sum(t.amount for t in tr_arr)


class AmountBalance:
    tr_arr: []
    gross_balance: [float]
    net_balance: [float]
    vat_balance: [float]

    def __init__(self, tr_arr):
        self.tr_arr = tr_arr
        self.gross_balance = self.__gross_balance(self.tr_arr)
        self.net_balance = self.__net_balance(self.tr_arr)
        self.vat_balance = self.__vat_balance(self.tr_arr)

    def __gross_balance(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.IN_TRANSFER:
                _sum += t.amount
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum -= t.amount
        return _sum

    def __net_balance(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.IN_TRANSFER:
                _sum += t.invoice.net_amount
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum -= t.amount
        return _sum

    def __vat_balance(self, tr_arr):
        return sum(t.invoice.vat_value for t in tr_arr
                   if t.transfer_type == TransferType.IN_TRANSFER)


def main():

    inv1 = DefaultVatInvoice(amount=1500.00, client="Burger King", worker="me", descr="data analysis")
    inv2 = NoVatInvoice(amount=2200, client="Biedronka", worker="me", descr="app")

    t1 = Transfer(TransferType.IN_TRANSFER, invoice=inv1, amount=1500.00,
                  _from="Burger Queen", _to="me", descr="data analysis")
    print(t1)
    t2 = Transfer(TransferType.IN_TRANSFER, invoice=inv2, amount=2200.00, _from="Burger King",
                  _to="me", descr="gift")

    t3 = Transfer(TransferType.OUT_TRANSFER, _to="Allegro", _from="me", amount=300)

    tr_arr = [t1, t2, t3]
    print(tr_arr)

    s = sum_transfers(tr_arr)
    print(s)

    s = sum_transfers_generator(tr_arr)
    print(s)
    print()
    balance = AmountBalance(tr_arr)

    print("brutto")
    print(balance.gross_balance)
    print("netto")
    print(balance.net_balance)
    print("vat")
    print(balance.vat_balance)


if __name__ == "__main__":
    main()
