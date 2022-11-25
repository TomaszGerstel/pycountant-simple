import datetime
from typing import List, Optional

from sqlalchemy import desc

from db import crud_receipt
from pycountant.model import Transfer
from pycountant.schemas import TransferSearch, TransferCreate


def get_all(session, user_id, limit=10) -> List[TransferSearch]:
    all_transfers = (
        session.query(Transfer).filter(Transfer.user_id == user_id).order_by(desc(Transfer.base_date)).limit(limit)
    )
    return all_transfers


def get_all_in_data_range(session, user_id, from_date, to_date) -> List[TransferSearch]:
    transfer_base = session.query(Transfer) \
        .filter(Transfer.user_id == user_id, Transfer.date > from_date - datetime.timedelta(days=1),
                Transfer.date < to_date + datetime.timedelta(days=1)) \
        .order_by(desc(Transfer.id))
    return transfer_base


def get(session, id, user_id) -> Optional[TransferSearch]:
    transfer = session.query(Transfer).filter(Transfer.id == id, Transfer.user_id == user_id,).first()
    if transfer is None:
        return None
    if transfer.receipt_id is not None:
        fill_in_incomplete_transaction_data(session, transfer, user_id)
    return transfer


def find_by_receipt_id(session, tr_id) -> Optional[TransferSearch]:
    transfer = session.query(Transfer).filter(Transfer.receipt_id == tr_id).first()
    return transfer


def fill_in_incomplete_transaction_data(session, transfer, user_id):
    receipt = crud_receipt.get(transfer.receipt_id, user_id, session)
    if receipt is None:
        return None
    if not transfer.from_:
        transfer.from_ = receipt.client
    if not transfer.to_:
        transfer.to_ = receipt.worker
    if not transfer.amount:
        transfer.amount = receipt.amount
    if not transfer.descr:
        transfer.descr = receipt.descr


def delete(session, tr_id):
    transfer = session.query(Transfer).filter(Transfer.id == tr_id).first()
    session.delete(transfer)
    session.commit()


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
        date=transfer.date,
        base_date=transfer.base_date,
        to_=transfer.to_,
        descr=transfer.descr,
        user_id=transfer.user_id
    )
    return trr_to_add
