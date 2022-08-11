from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from db.session import Session, engine
from pycountant.model import Receipt
from pycountant.schemas import ReceiptSearch


def get_all(session) -> List[ReceiptSearch]:
    # obj_in_data = jsonable_encoder(obj_in)
    receipts_base = session.query(Receipt).all();
    receipts_to_display = []
    for receipt in receipts_base:
        receipts_to_display.append(map_to_receipt_search(receipt))
    return receipts_to_display


def get(id, session) -> Optional[ReceiptSearch]:
    # session = Session(bind=engine)
    rec_base = session.query(Receipt).filter(Receipt.id == id).first()
    rec_to_display = map_to_receipt_search(rec_base)
    #     id=rec_base.id,
    #     amount=rec_base.amount,
    #     client=rec_base.client,
    #     worker=rec_base.worker,
    #     vat_value=rec_base.vat_value,
    #     net_amount=rec_base.net_amount,
    #     vat_percentage=rec_base.vat_percentage,
    #     descr=rec_base.descr
    # )
    return rec_to_display


def map_to_receipt_search(receipt):
    rec_to_display = ReceiptSearch(
        id=receipt.id,
        amount=receipt.amount,
        client=receipt.client,
        worker=receipt.worker,
        vat_value=receipt.vat_value,
        net_amount=receipt.net_amount,
        vat_percentage=receipt.vat_percentage,
        descr=receipt.descr
    )
    return rec_to_display

