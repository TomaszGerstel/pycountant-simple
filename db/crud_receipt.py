from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from db.session import Session, engine
from model import Receipt
from schemas import ReceiptSearch


# def get_all() -> List[ReceiptSearch]:
#     session = Session(bind=engine)
#     # obj_in_data = jsonable_encoder(obj_in)
#     return session.query(ReceiptSearch).all()

def get(id, session) -> Optional[ReceiptSearch]:
    # session = Session(bind=engine)
    receipt = session.query(Receipt).filter(Receipt.id == id).first()
    return receipt



