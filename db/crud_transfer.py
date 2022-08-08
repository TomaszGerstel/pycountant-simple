from typing import List, Optional
from fastapi.encoders import jsonable_encoder

import crud_receipt
from model import Transfer
from db.session import Session, engine
from schemas import TransferSearch

local_session = Session(bind=engine)


def get_all() -> List[TransferSearch]:
    all_transfers = local_session.query(Transfer).all()
    # for bt in all_transfers:
    #     bt.receipt = crud_receipt.get(bt.receipt_id, session)
    return all_transfers


def get(id) -> Optional[TransferSearch]:
    transfer = local_session.query(Transfer).filter(Transfer.id == id).first()
    fill_in_incomplete_transaction_data(transfer)
    # transfer.receipt = crud_receipt.get(transfer.receipt_id, session)
    json_transfer = jsonable_encoder(transfer)
    return json_transfer


def fill_in_incomplete_transaction_data(transfer):
    receipt = crud_receipt.get(transfer.receipt_id, local_session)
    if not transfer.from_:
        transfer.from_ = receipt.client
    if not transfer.to_:
        transfer.to_ = receipt.worker
    if not transfer.amount:
        transfer.amount = receipt.amount
    if transfer.descr == "":
        transfer.descr = receipt.descr