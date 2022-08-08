from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from db.session import Session, engine
from pycountant.model import Receipt
from pycountant.schemas import ReceiptSearch


# def get_all() -> List[ReceiptSearch]:
#     session = Session(bind=engine)
#     # obj_in_data = jsonable_encoder(obj_in)
#     return session.query(ReceiptSearch).all()

def get(id, session) -> Optional[ReceiptSearch]:
    # session = Session(bind=engine)
    rec_base = session.query(Receipt).filter(Receipt.id == id).first()
    rec_to_display = ReceiptSearch(
        id=rec_base.id,
        amount=rec_base.amount,
        client=rec_base.client,
        worker=rec_base.worker,
        vat_value=rec_base.vat_value,
        net_amount=rec_base.net_amount,
        vat_percentage=rec_base.vat_percentage,
        descr=rec_base.descr
    )
    return rec_to_display



