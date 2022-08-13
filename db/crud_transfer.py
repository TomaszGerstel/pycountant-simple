from typing import List, Optional

from sqlalchemy import desc

from db import crud_receipt
from pycountant.model import Transfer
from pycountant.schemas import TransferSearch, TransferCreate


def get_all(session, limit=10) -> List[TransferSearch]:
    all_transfers = (
        session.query(Transfer).order_by(desc(Transfer.id)).limit(limit).all()
    )
    return all_transfers


def get(session, id) -> Optional[TransferSearch]:
    transfer = session.query(Transfer).filter(Transfer.id == id).first()
    fill_in_incomplete_transaction_data(session, transfer)
    return transfer


def fill_in_incomplete_transaction_data(session, transfer):
    receipt = crud_receipt.get(transfer.receipt_id, session)
    if not transfer.from_:
        transfer.from_ = receipt.client
    if not transfer.to_:
        transfer.to_ = receipt.worker
    if not transfer.amount:
        transfer.amount = receipt.amount
    if not transfer.descr:
        transfer.descr = receipt.descr


def create(transfer_create: TransferCreate, session) -> Transfer:
    db_trr = map_to_transfer_base(transfer_create)
    session.add(db_trr)
    session.commit()
    session.refresh(db_trr)
    return db_trr


def map_to_transfer_base(transfer):
    trr_to_add = Transfer(
        transfer_type=transfer.transfer_type,
        amount=transfer.amount,
        receipt_id=transfer.receipt_id,
        from_=transfer.from_,
        to_=transfer.to_,
        descr=transfer.descr,
    )
    return trr_to_add
