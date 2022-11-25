import os

from fastapi_login.fastapi_login import LoginManager

from db import crud_user


from db.session import Session

SECRET = os.urandom(24).hex()
session = Session()
manager = LoginManager(SECRET, token_url="/login")
manager.cookie_name = "app-token-cookie"
current_user_id = None
lump_sum_tax_rate = None
current_user_name = None


@manager.user_loader
def load_user(username):
    user = crud_user.get(name=username, session=session)
    return user
