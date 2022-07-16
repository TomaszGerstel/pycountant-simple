from model import TransferType
from exceptions import NegativeValueError
from config import config


class BalanceOfFinances:
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

    def __repr__(self):
        return (
            f"\ncosts:{self.costs}; gross income:{self.gross_income}; balance: {self.balance}\n"
            f"net balance: {self.net_balance}; vat balance: {self.vat_balance}\n"
            f"income tax: {self.income_tax_30}; profit: {self.profit}\n"
        )

    def __get_costs(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.transfer_type == TransferType.OUT_TRANSFER:
                _sum += t.invoice.amount
        return _sum

    def __gross_income(self, tr_arr):
        _sum = 0
        for t in tr_arr:
            if t.amount <= 0:
                raise NegativeValueError("amount can't be negative value")
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
        return income * config.income_tax_pct / 100.0
