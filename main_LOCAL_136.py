import datetime
from dataclasses import dataclass
from typing import Optional


class Transfer1:
    def __init__(self, amout, _from, _to):
        self.amout = amout
        self._from = _from
        self._to = _to

@dataclass
class Invoice:
    amount: float
    client: str
    worker: str
    date: datetime = datetime.date.today()
    descr: str = ""

@dataclass
class Transfer:
    invoice: Optional[Invoice] = None
    amount: Optional[float] = None
    _from: Optional[str] = None
    _to: Optional[str] = None
    date: datetime.datetime = datetime.date.today()
    descr: str = ""

    def __post_init__(self):
        if self.invoice is not None:
            self._from = self.invoice.client
            self._to = self.invoice.worker
            self.amount = self.invoice.amount

    def __repr__(self):
        core_repr = f"On {self.date} {self._from} sent {self.amount} to {self._to}"
        if self.descr != "":
            return core_repr + f" for {self.descr}"
        return core_repr

def sum_transfer(tr_arr):
    _sum = 0
    for t in tr_arr:
        _sum += t.amount
    return _sum

def sum_transfer_generator(tr_arr):
    return sum(t.amount for t in tr_arr)

def main():

    inv1 = Invoice(amount=300.00, client="Burger King", worker="me", descr="za bułki")

    t = Transfer(invoice=inv1, amount=500.00, _from="McDonalds", _to="me")
    print(t)
    t2 = Transfer(amount=500.00, _from="McDonalds", _to="me", descr="obiad")
    print(t2)

    tr_arr = [t, t2]

    s = sum_transfer_generator(tr_arr)
    print(s)

if __name__ == "__main__":
    main()