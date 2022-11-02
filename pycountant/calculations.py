import datetime
from dataclasses import dataclass

from db import crud_transfer, crud_receipt
from pycountant.schemas import TransferType, TransactionToCalculate
from pycountant.exceptions import NegativeValueError
from pycountant.config import config
import calendar


@dataclass
class BalanceResults:
    costs: float
    other_costs: float
    gross_income: float
    balance: float
    due_vat: float
    due_tax_30: float
    net_balance: float
    vat_balance: float

    income_tax_30: float
    due_profit: float
    remaining_profit: float
    paid_profit: float
    paid_vat: float
    paid_tax: float

    def __repr__(self):
        return (
            f"\ncosts:{self.costs}; other costs:{self.other_costs}; gross income:{self.gross_income}\n"
            f"balance: {self.balance}; net balance: {self.net_balance}\n"
            f"vat balance: {self.vat_balance}; due vat: {self.due_vat}; vat paid: {self.paid_vat}\n"
            f"tax balance: {self.income_tax_30}; due tax: {self.due_tax_30}; tax paid: {self.paid_tax}\n"
            f"remaining profit: {self.remaining_profit}; due profit: {self.due_profit}; profit paid: {self.paid_profit}\n"
        )


def current_balance(session, user_id):
    tr_arr = crud_transfer.get_all(session, user_id, -1)
    rec_arr = crud_receipt.get_all(session, user_id)
    return calculate_balance(tr_arr, rec_arr)


def balance_to_month(session, user_id, months_back=0):

    month = datetime.datetime.today().month
    year = datetime.datetime.today().year
    month_range = calendar.monthrange(year, month)
    first_day = datetime.date(year, month, 1)
    last_day = first_day + datetime.timedelta(days=month_range[1]-1)

    if months_back > 0:
        ran = range(months_back)
        for n in ran:
            last_day = first_day - datetime.timedelta(days=1)
            month_range = calendar.monthrange(last_day.year, last_day.month)
            first_day = last_day - datetime.timedelta(days=month_range[1]-1)

    return balance_to_date_range(session, user_id, first_day, last_day), first_day, last_day


def balance_to_date_range(session, user_id, from_date, to_date):
    if from_date > to_date:
        return None
    tr_arr = crud_transfer.get_all_in_data_range(session, user_id, from_date, to_date)
    rec_arr = crud_receipt.get_all_in_date_range(session, user_id, from_date, to_date)
    return calculate_balance(tr_arr, rec_arr)


def calculate_balance(tr_arr_given, rec_arr_given) -> BalanceResults:

    tr_arr = create_transaction_objects(tr_arr_given, rec_arr_given)

    costs = get_costs(tr_arr)
    gross_income = get_gross_income(tr_arr)
    paid_profit = get_paid_profit(tr_arr)
    net_balance = get_net_balance(tr_arr)
    due_vat = get_due_vat_balance(tr_arr)
    due_tax_30 = get_due_income_tax_30(net_balance)
    paid_vat = get_paid_vat(tr_arr)
    paid_tax = get_paid_tax(tr_arr)
    vat_balance = due_vat - paid_vat
    income_tax_30 = due_tax_30 - paid_tax
    due_profit = net_balance - due_tax_30
    remaining_profit = due_profit - paid_profit
    other_costs = paid_vat + paid_tax + paid_profit
    balance = gross_income - costs - other_costs

    return BalanceResults(
        costs=costs,
        other_costs=other_costs,
        gross_income=gross_income,
        balance=balance,
        net_balance=net_balance,
        vat_balance=vat_balance,
        income_tax_30=income_tax_30,
        due_vat=due_vat,
        due_tax_30=due_tax_30,
        due_profit=due_profit,
        paid_profit=paid_profit,
        paid_vat=paid_vat,
        paid_tax=paid_tax,
        remaining_profit=remaining_profit,
    )


def create_transaction_objects(tr_arr, rec_arr):
    transactions = []
    for tr in tr_arr:
        for rec in rec_arr:
            if tr.receipt_id == rec.id:
                transaction = TransactionToCalculate(
                    amount=rec.amount,
                    transfer_type=tr.transfer_type,
                    vat_value=rec.vat_value,
                    net_amount=rec.net_amount,
                    vat_percentage=rec.vat_percentage,
                )
                transactions.append(transaction)
        if tr.transfer_type == TransferType.VAT_OUT_TRANSFER \
                or tr.transfer_type == TransferType.TAX_OUT_TRANSFER \
                or tr.transfer_type == TransferType.SALARY:
            transaction = TransactionToCalculate(
                amount=tr.amount,
                transfer_type=tr.transfer_type
            )
            transactions.append(transaction)
    return transactions


def get_costs(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_gross_income(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.amount <= 0:
            raise NegativeValueError("amount can't be negative value")
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_net_balance(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.net_amount
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.net_amount
    return _sum.__round__(2)


def get_paid_profit(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.SALARY:
            _sum += t.amount
    return _sum.__round__(2)


def get_paid_vat(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.VAT_OUT_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_paid_tax(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.TAX_OUT_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_due_vat_balance(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.vat_value
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.vat_value
    return _sum.__round__(2)


def get_due_income_tax_30(income):
    return (income * config.income_tax_pct / 100.0).__round__(2)
