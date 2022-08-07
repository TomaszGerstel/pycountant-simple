from typing import List, Optional
from fastapi.encoders import jsonable_encoder

import crud_receipt
from model import Transfer
from db.session import Session, engine
from schemas import TransferSearch

session = Session(bind=engine)


def get_all() -> List[TransferSearch]:
    all_transfers = session.query(Transfer).all()
    # for bt in all_transfers:
    #     bt.receipt = crud_receipt.get(bt.receipt_id, session)
    return all_transfers


def get(id) -> Optional[TransferSearch]:
    transfer = session.query(Transfer).filter(Transfer.id == id) \
        .first()
    transfer.receipt = crud_receipt.get(transfer.receipt_id, session)
    json_transfer = jsonable_encoder(transfer)
    return json_transfer
