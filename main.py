import datetime
from dataclasses import dataclass
from typing import Optional

from enum import Enum

from exceptions import NegativeValueError


class Client(Enum):
    MCDONALDS = "McDonald's"


class TransferTaxType(Enum):
    DEFAULT_VAT_TRANSFER = "Default VAT transfer 30%"
    FIXED_VAT_TRANSFER = "Fixed VAT transfer"
    NO_VAT_TRANSFER = "No VAT transfer"


class TransferType(Enum):
    IN_TRANSFER = "Incoming transfer"
    OUT_TRANSFER = "Outgoing transfer"


@dataclass
class Invoice:
    amount: float
    client: str
    worker: str
    date: datetime = datetime.date.today()  # zmienic
    descr: str = ""


@dataclass
class Transfer:
    transfer_type: TransferType
    transfer_tax_type: TransferTaxType
    invoice: Invoice = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    amount: Optional[float] = None
    net_amount: [float] = None
    vat: [float] = None
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

        self.net_amount = self.__set_net_amount()

    def __set_net_amount(self):
        if self.transfer_tax_type == TransferTaxType.NO_VAT_TRANSFER:
            return self.amount
        if self.transfer_tax_type == TransferTaxType.DEFAULT_VAT_TRANSFER:
            return self.amount / (100 + 30) * 100
        if self.transfer_tax_type == TransferTaxType.FIXED_VAT_TRANSFER:
            return self.vat


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
                _sum += t.net_amount
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum -= t.net_amount
        return _sum

    def __vat_balance(self, tr_arr):
        return self.__gross_balance(tr_arr) - self.__net_balance(tr_arr)

def main():
    inv1 = Invoice(amount=500.00, client="Burger King", worker="me", descr="data analysis")
    print(inv1)
    t2 = Transfer(TransferType.IN_TRANSFER, TransferTaxType.DEFAULT_VAT_TRANSFER, invoice=inv1, amount=500.00,
                  _from="Burger Queen", _to="me", descr="data analysis")
    print(t2)
    t3 = Transfer(TransferType.OUT_TRANSFER, TransferTaxType.NO_VAT_TRANSFER, amount=1500.00, _from="me",
                  _to="Burger King", descr="gift")
    tr_arr = [t2, t3]
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
