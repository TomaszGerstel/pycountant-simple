from db.session import Session, engine
from pycountant.model import Receipt, Transfer, User
from pycountant.sample_data import RECEIPTS_ANY, TRANSFERS_ANY, USERS_ANY

local_session = Session(bind=engine)


def add_sample_data():
    for ur in USERS_ANY:
        new_user = User(
            id=ur["id"],
            name=ur["name"],
            password=ur["password"],
            email=ur["email"]
        )
        local_session.add(new_user)
        local_session.commit()
    for rec in RECEIPTS_ANY:
        new_receipt = Receipt(
            amount=rec["amount"],
            vat_percentage=rec["vat_percentage"],
            client=rec["client"],
            worker=rec["worker"],
            descr=rec["descr"],
            user_id=rec["user_id"],
        )
        local_session.add(new_receipt)
        local_session.commit()

    for tr in TRANSFERS_ANY:
        new_transfer = Transfer(
            transfer_type=tr["transfer_type"],
            amount=tr["amount"],
            receipt_id=tr["receipt_id"],
            from_=tr["from_"],
            to_=tr["to_"],
            descr=tr["descr"],
            user_id=tr["user_id"],
        )
        local_session.add(new_transfer)
        local_session.commit()


if __name__ == "__main__":
    add_sample_data()
