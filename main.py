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


def sum_transfers(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.amount <= 0:
            raise NegativeValueError("amount can't be negative value")
        _sum += t.amount
    return _sum


def sum_transfers_generator(tr_arr):
    return sum(t.amount for t in tr_arr)


class AmountBalance:
    tr_arr: []
    costs: [float]
    gross_income: [float]
    balance: [float]
    net_balance: [float]
    vat_balance: [float]
    # income_tax_11: [float]
    income_tax_30: [float]
    profit: [float]

    def __init__(self, tr_arr):
        self.tr_arr = tr_arr
        self.costs = self.__get_costs(self.tr_arr)
        self.gross_income = self.__gross_income(self.tr_arr)
        self.balance = self.gross_income - self.costs
        self.net_balance = self.__net_balance(self.tr_arr)
        self.vat_balance = self.__vat_balance(self.tr_arr)
        self.income_tax_30 = self.__calc_income_tax_30(self.net_balance)
        self.profit = self.net_balance - self.income_tax_30

    def __get_costs(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum += t.invoice.amount
        return _sum

    def __gross_income(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.IN_TRANSFER:
                _sum += t.amount
        return _sum

    def __net_balance(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.IN_TRANSFER:
                _sum += t.invoice.net_amount
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum -= t.invoice.net_amount
        return _sum

    def __vat_balance(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.IN_TRANSFER:
                _sum += t.invoice.vat_value
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum -= t.invoice.vat_value
        return _sum

    def __calc_income_tax_30(self, income):
        return income * 0.3



def main():

    inv1 = DefaultVatInvoice(amount=1500.00, client="Burger King", worker="me", descr="data analysis")
    inv2 = NoVatInvoice(amount=2200, client="Biedronka", worker="me", descr="app")
    inv3 = DefaultVatInvoice(amount=300, client="me", worker="Allegro", descr="for hard_drive")

    t1 = Transfer(TransferType.IN_TRANSFER, invoice=inv1, amount=1500.00,
                  _from="Burger Queen", _to="me", descr="data analysis")
    print(t1)
    t2 = Transfer(TransferType.IN_TRANSFER, invoice=inv2, amount=2200.00, _from="Burger King",
                  _to="me", descr="gift")
    t3 = Transfer(TransferType.OUT_TRANSFER, invoice=inv3, _to="Allegro", _from="me", amount=300)
    tr_arr = [t1, t2, t3]
    balance = AmountBalance(tr_arr)
    print()
    print("Calculations for: Incoming transfer based on invoices", inv1.amount, "with default vat = 30% and",
          inv2.amount, "with 0 vat and one outgoing transfer for", inv3.amount, "with default vat = 30%:")

    print()
    print("state of finances (balance), should equals income - costs:")
    print(balance.balance)
    print()
    print("income:")
    print(balance.gross_income)
    print()
    print("costs (outgoing):")
    print(balance.costs)
    print()
    print("net profit (less costs and VAT):")
    print(balance.net_balance)
    print()
    print("vat (to the treasury):")
    print(balance.vat_balance)
    print()
    print("income tax to the tax office (30%):")
    print(balance.income_tax_30)
    print()
    print("profit after tax:")
    print(balance.profit)


if __name__ == "__main__":
    main()
