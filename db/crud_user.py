from typing import List, Optional

from pycountant.model import User
from pycountant.schemas import UserSearch


def get_all(session) -> List[UserSearch]:
    users_base = session.query(User).all()
    users_to_display = []
    for user in users_base:
        users_to_display.append(map_to_user_search(user))
    return users_to_display


def get(name, session) -> Optional[UserSearch]:
    user_to_display = None
    user_base = session.query(User).filter(User.name == name).first()
    if user_base is not None:
        user_to_display = map_to_user_search(user_base)

    return user_to_display


# def delete(session, rec_id):
#     receipt = session.query(Receipt).filter(Receipt.id == rec_id).first()
#     transfer = crud_transfer.find_by_receipt_id(session=session, tr_id=rec_id)
#     if transfer is not None:
#         crud_transfer.delete(session=session, tr_id=transfer.id)
#     session.delete(receipt)
#     session.commit()


# def create(receipt_create: ReceiptCreate, session) -> Receipt:
#     db_receipt = map_to_receipt_base(receipt_create)
#     session.add(db_receipt)
#     session.commit()
#     session.refresh(db_receipt)
#     return db_receipt


def map_to_user_search(user):
    user_to_display = UserSearch(
        id=user.id,
        password=user.password,
        name=user.name,
        email=user.email,
    )
    return user_to_display
