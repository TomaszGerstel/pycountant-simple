from sqlalchemy import Column, Integer, Float, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from pycountant.schemas import TransferType

Base = declarative_base()


class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer(), primary_key=True)
    amount = Column(Float(), nullable=False)
    client = Column(String(80), nullable=False)
    worker = Column(String(80), nullable=False)
    vat_value = Column(Float(), nullable=True)
    net_amount = Column(Float(), nullable=True)
    vat_percentage = Column(Float(), nullable=True)
    descr = Column(String(80), nullable=False)

    def __repr__(self):
        return (
            f"Receipt from: {self.worker} to: {self.client} with amount: {self.amount}"
            f"for {self.descr}"
        )


class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer(), primary_key=True)
    transfer_type = Column(Enum(TransferType), nullable=False)
    amount = Column(Float(), nullable=True)
    from_ = Column(String(80), nullable=True)
    to_ = Column(String(80), nullable=True)
    date = Column(DateTime(), default=datetime.utcnow())
    descr = Column(String(80), nullable=True)
    receipt_id = Column(Integer(), ForeignKey("receipts.id"), nullable=False)
    receipt = relationship("Receipt")

    def __repr__(self):
        return (
            f"{self.transfer_type} from: {self.from_} to {self.to_}"
            f"with amount {self.amount}"
            f" for {self.descr}"
        )
