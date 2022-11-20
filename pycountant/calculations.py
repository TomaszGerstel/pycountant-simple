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
    net_balance: float
    vat_due: float
    vat_paid: float
    vat_balance: float
    flat_tax_due: float
    tax_paid: float
    flat_tax_balance: float
    lump_tax_rate: float
    lump_sum_tax_due: float
    lump_sum_tax_balance: float
    profit_due_flat: float
    profit_remaining_flat: float
    profit_due_lump: float
    profit_remaining_lump: float
    profit_paid: float    

    def __str__(self):
        return (
            f"\ncosts:{self.costs}; other costs:{self.other_costs}; gross income:{self.gross_income}\n"
            f"balance: {self.balance}; net balance: {self.net_balance}\n"
            f"vat balance: {self.vat_balance}; due vat: {self.vat_due}; vat paid: {self.vat_paid}\n"
            f"tax balance: {self.flat_tax_balance}; due tax: {self.flat_tax_due}; tax paid: {self.tax_paid}\n"
            f"lump tax balance: {self.lump_sum_tax_balance}; due lump-sum tax: {self.lump_sum_tax_due};"           
            f"remaining profit: {self.profit_remaining_flat}; due profit: {self.profit_due_flat}; "
            f"profit paid: {self.profit_paid}\n"
        )


def current_balance(session, user_id, lump_sum_tax_rate):
    tr_arr = crud_transfer.get_all(session, user_id, -1)
    rec_arr = crud_receipt.get_all(session, user_id)
    return calculate_balance(tr_arr, rec_arr, lump_sum_tax_rate)


def balance_to_month(session, user_id, lump_sum_tax_rate, months_back=0, ):

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

    return balance_to_date_range(session, user_id, first_day, last_day, lump_sum_tax_rate), first_day, last_day


def balance_to_date_range(session, user_id, from_date, to_date, lump_sum_tax_rate):
    if from_date > to_date:
        return None
    tr_arr = crud_transfer.get_all_in_data_range(session, user_id, from_date, to_date)
    rec_arr = crud_receipt.get_all_in_date_range(session, user_id, from_date, to_date)
    return calculate_balance(tr_arr, rec_arr, lump_sum_tax_rate)


def calculate_balance(tr_arr_given, rec_arr_given, lump_sum_tax_rate=None) -> BalanceResults:

    tr_arr = create_transaction_objects(tr_arr_given, rec_arr_given)

    costs = get_costs(tr_arr)
    gross_income = get_gross_income(tr_arr)
    profit_paid = get_profit_paid(tr_arr)
    net_balance = get_net_balance(tr_arr)
    vat_due = get_vat_due(tr_arr)
    flat_tax_due = get_due_flat_tax(net_balance)
    lump_tax_rate = get_lump_sum_tax_rate(lump_sum_tax_rate)
    lump_sum_tax_due = get_lump_sum_tax_due(gross_income, lump_tax_rate)
    vat_paid = get_vat_paid(tr_arr)
    tax_paid = get_tax_paid(tr_arr)
    vat_balance = vat_due - vat_paid
    flat_tax_balance = flat_tax_due - tax_paid
    lump_sum_tax_balance = (lump_sum_tax_due - tax_paid).__round__(2)
    profit_due_flat = net_balance - flat_tax_due
    profit_remaining_flat = profit_due_flat - profit_paid
    profit_due_lump = net_balance - lump_sum_tax_due
    profit_remaining_lump = profit_due_lump - profit_paid
    other_costs = vat_paid + tax_paid + profit_paid
    balance = gross_income - costs - other_costs

    return BalanceResults(
        costs=costs,
        other_costs=other_costs,
        gross_income=gross_income,
        balance=balance,
        net_balance=net_balance,
        vat_balance=vat_balance,
        flat_tax_balance=flat_tax_balance,
        vat_due=vat_due,
        flat_tax_due=flat_tax_due,
        lump_tax_rate=lump_tax_rate,
        lump_sum_tax_due=lump_sum_tax_due,
        lump_sum_tax_balance=lump_sum_tax_balance,
        profit_due_flat=profit_due_flat,
        profit_due_lump=profit_due_lump,
        profit_paid=profit_paid,
        vat_paid=vat_paid,
        tax_paid=tax_paid,
        profit_remaining_flat=profit_remaining_flat,
        profit_remaining_lump=profit_remaining_lump
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


def get_profit_paid(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.SALARY:
            _sum += t.amount
    return _sum.__round__(2)


def get_vat_paid(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.VAT_OUT_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_tax_paid(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.TAX_OUT_TRANSFER:
            _sum += t.amount
    return _sum.__round__(2)


def get_vat_due(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.vat_value
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.vat_value
    return _sum.__round__(2)


def get_due_flat_tax(income):
    return (income * config.income_flat_tax_pct / 100.0).__round__(2)


def get_lump_sum_tax_rate(tax_rate_from_user):
    if tax_rate_from_user is not None:
        return tax_rate_from_user
    return config.default_lump_sum_tax_rate


def get_lump_sum_tax_due(income, tax_rate):
    return (income * tax_rate / 100.0).__round__(2)
