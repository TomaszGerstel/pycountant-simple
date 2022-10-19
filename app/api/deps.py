from db import crud_transfer, crud_receipt, crud_user
from pycountant.calculations import current_balance

from db.session import Session

session = Session()


def get_transfers():
    return crud_transfer.get_all(session, 10)


def get_receipts():
    return crud_receipt.get_all(session)


def get_balance():
    print("TYPE:", current_balance(session))
    return current_balance(session)


# def get_user(name):
#     return crud_user.get(name, session)
