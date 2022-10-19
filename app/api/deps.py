import os

from fastapi_login.fastapi_login import LoginManager

from db import crud_transfer, crud_receipt, crud_user
from pycountant.calculations import current_balance

from db.session import Session

SECRET = os.urandom(24).hex()
session = Session()
manager = LoginManager(SECRET, token_url="/login")
manager.cookie_name = "app-token-cookie"
current_user_id = manager.current_user_id


@manager.user_loader
def load_user(username):
    user = crud_user.get(name=username, session=session)
    return user


def get_transfers():
    return crud_transfer.get_all(session, current_user_id, 10)


def get_receipts():
    return crud_receipt.get_all(session, current_user_id)


def get_balance():
    # print("TYPE:", current_balance(session))
    return current_balance(session, current_user_id)


def get_receipts_without_transfer():
    return crud_receipt.get_all_without_transfer(session, current_user_id)

# def get_user(name):
#     return crud_user.get(name, session)
