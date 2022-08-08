from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from db import crud_receipt
from pycountant.model import Transfer
from pycountant.schemas import TransferSearch

# local_session = Session(bind=engine)


def get_all(session, limit) -> List[TransferSearch]:
    all_transfers = session.query(Transfer).limit(limit).all()
    return all_transfers


def get(session, id) -> Optional[TransferSearch]:
    transfer = session.query(Transfer).filter(Transfer.id == id).first()
    fill_in_incomplete_transaction_data(session, transfer)
    # json_transfer = jsonable_encoder(transfer)
    return transfer


def fill_in_incomplete_transaction_data(session, transfer):
    receipt = crud_receipt.get(transfer.receipt_id, session)
    if not transfer.from_:
        transfer.from_ = receipt.client
    if not transfer.to_:
        transfer.to_ = receipt.worker
    if not transfer.amount:
        transfer.amount = receipt.amount
    if transfer.descr == "":
        transfer.descr = receipt.descr