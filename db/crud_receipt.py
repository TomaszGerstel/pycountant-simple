from typing import List, Optional

from sqlalchemy import desc

from db import crud_transfer
from pycountant.model import Receipt
from pycountant.schemas import ReceiptSearch, ReceiptCreate


def get_all(session, user_id) -> List[ReceiptSearch]:
    receipts_base = session.query(Receipt).filter(Receipt.user_id == user_id).order_by(desc(Receipt.id)).all()
    receipts_to_display = []
    for receipt in receipts_base:
        receipts_to_display.append(map_to_receipt_search(receipt))
    return receipts_to_display


# all recipes that have not been used in any transfer
def get_all_without_transfer(session, user_id) -> List[ReceiptSearch]:
    all_receipts = get_all(session, user_id)
    all_not_used_rec = []
    all_transfers = crud_transfer.get_all(session, user_id, -1)
    receipt_keys = set()

    for trr in all_transfers:
        receipt_keys.add(trr.receipt_id)

    for rec in all_receipts:
        if rec.id not in receipt_keys:
            all_not_used_rec.append(rec)

    return all_not_used_rec


def get(id, session) -> Optional[ReceiptSearch]:
    rec_base = session.query(Receipt).filter(Receipt.id == id).first()
    rec_to_display = map_to_receipt_search(rec_base)
    return rec_to_display


def delete(session, rec_id):
    receipt = session.query(Receipt).filter(Receipt.id == rec_id).first()
    transfer = crud_transfer.find_by_receipt_id(session=session, tr_id=rec_id)
    if transfer is not None:
        crud_transfer.delete(session=session, tr_id=transfer.id)
        session.commit()
    session.delete(receipt)
    session.commit()


def create(receipt_create: ReceiptCreate, session) -> Receipt:
    db_receipt = map_to_receipt_base(receipt_create)
    session.add(db_receipt)
    session.commit()
    session.refresh(db_receipt)
    return db_receipt


def map_to_receipt_search(receipt):
    rec_to_display = ReceiptSearch(
        id=receipt.id,
        amount=receipt.amount,
        client=receipt.client,
        worker=receipt.worker,
        vat_value=receipt.vat_value,
        net_amount=receipt.net_amount,
        vat_percentage=receipt.vat_percentage,
        descr=receipt.descr,
    )
    return rec_to_display


def map_to_receipt_base(receipt):
    rec_to_add = Receipt(
        amount=receipt.amount,
        client=receipt.client,
        worker=receipt.worker,
        vat_value=receipt.vat_value,
        net_amount=receipt.net_amount,
        vat_percentage=receipt.vat_percentage,
        descr=receipt.descr,
        user_id=receipt.user_id,
    )
    return rec_to_add
