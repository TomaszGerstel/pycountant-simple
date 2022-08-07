from typing import List
from fastapi.encoders import jsonable_encoder

import crud_receipt
from model import Transfer
from db.session import Session, engine
from schemas import TransferSearch, TransferType


def get_all() -> List[TransferSearch]:
    session = Session(bind=engine)
    transfers_from_base = session.query(Transfer).all()
    transfers_search = []
    for bt in transfers_from_base:
        new_ts = TransferSearch(
            id=bt.id,
            transfer_type=bt.transfer_type,
            amount=bt.amount,
            receipt_id=bt.receipt_id,
            from_=bt.from_,
            to_=bt.to_,
            date=bt.date,
            descr=bt.descr
        )
        new_ts.receipt = crud_receipt.get(new_ts.receipt_id)
        transfers_search.append(new_ts)

    return transfers_search


