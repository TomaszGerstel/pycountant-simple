from dataclasses import dataclass

from pycountant.schemas import TransferType
from pycountant.exceptions import NegativeValueError
from pycountant.config import config


@dataclass
class BalanceResults:
    costs: float
    gross_income: float
    balance: float
    net_balance: float
    vat_balance: float
    # income_tax_11: float
    income_tax_30: float
    profit: float

    def __repr__(self):
        return (
            f"\ncosts:{self.costs}; gross income:{self.gross_income}\n"
            f"balance: {self.balance}\n"
            f"net balance: {self.net_balance}; vat balance: {self.vat_balance}\n"
            f"income tax: {self.income_tax_30}; profit: {self.profit}\n"
        )


def calculate_balance(tr_arr_given, rec_arr_given) -> BalanceResults:

    tr_with_rec_arr = put_receipt_into_transfer(tr_arr_given, rec_arr_given)
    tr_arr = fill_in_incomplete_transaction_data(tr_with_rec_arr)

    costs = get_costs(tr_arr)
    gross_income = get_gross_income(tr_arr)
    balance = gross_income - costs
    net_balance = get_net_balance(tr_arr)
    vat_balance = get_vat_balance(tr_arr)
    income_tax_30 = get_calc_income_tax_30(net_balance)
    profit = net_balance - income_tax_30
    return BalanceResults(
        costs=costs,
        gross_income=gross_income,
        balance=balance,
        net_balance=net_balance,
        vat_balance=vat_balance,
        income_tax_30=income_tax_30,
        profit=profit,
    )


def put_receipt_into_transfer(tr_arr, rec_arr):
    for tr in tr_arr:
        for rec in rec_arr:
            if tr.receipt_id == rec.id:
                tr.receipt = rec
    return tr_arr


def fill_in_incomplete_transaction_data(tr_arr):
    for tr in tr_arr:
        if tr.receipt is not None:
            if not tr.from_:
                tr.from_ = tr.receipt.client
            if not tr.to_:
                tr.to_ = tr.receipt.worker
            if not tr.amount:
                tr.amount = tr.receipt.amount
            if tr.descr == "":
                tr.descr = tr.receipt.descr
    return tr_arr


def get_costs(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum += t.receipt.amount
    return _sum


def get_gross_income(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.amount <= 0:
            raise NegativeValueError("amount can't be negative value")
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.amount
    return _sum


def get_net_balance(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.receipt.net_amount
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.receipt.net_amount
    return _sum


def get_vat_balance(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.receipt.vat_value
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.receipt.vat_value
    return _sum


def get_calc_income_tax_30(income):
    return income * config.income_tax_pct / 100.0

