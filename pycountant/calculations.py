from dataclasses import dataclass

from db import crud_transfer, crud_receipt
from pycountant.schemas import TransferType, TransactionToCalculate
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


def current_balance(session, user_id):
    tr_arr = crud_transfer.get_all(session, user_id, -1)
    rec_arr = crud_receipt.get_all(session, user_id)
    return calculate_balance(tr_arr, rec_arr)


def balance_to_date_range(session, user_id, from_date, to_date):
    tr_arr = crud_transfer.get_all(session, user_id, -1)
    rec_arr = crud_receipt.get_all_in_date_range(session, user_id, from_date, to_date)
    return calculate_balance(tr_arr, rec_arr)


def calculate_balance(tr_arr_given, rec_arr_given) -> BalanceResults:

    tr_arr = create_transaction_objects(tr_arr_given, rec_arr_given)

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
                or tr.transfer_type == TransferType.TAX_OUT_TRANSFER:
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


def get_vat_balance(tr_arr):
    _sum = 0
    for t in tr_arr:
        if t.transfer_type == TransferType.IN_TRANSFER:
            _sum += t.vat_value
        if t.transfer_type == TransferType.OUT_TRANSFER:
            _sum -= t.vat_value
    return _sum.__round__(2)


def get_calc_income_tax_30(income):
    return (income * config.income_tax_pct / 100.0).__round__(2)
