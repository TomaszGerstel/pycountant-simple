from pycountant.model import Receipt, Transfer, TransferType

# Simulate database
from schemas import ReceiptSearch, TransferSearch

RECEIPTS_ANY = [
    {
        "id": 1,
        "amount": 1300.0,
        "vat_percentage": 30,
        "client": "Burger King",
        "worker": "me",
        "descr": "data analysis",
    },
    {
        "id": 2,
        "amount": 4800.0,
        "client": "NSA",
        "worker": "me",
        "descr": "secret data wrangling",
        "vat_percentage": 20,
    },
    {
        "id": 3,
        "amount": 800.0,
        "vat_percentage": 30,
        "client": "me",
        "worker": "they",
        "descr": "stuff",
    }
]

TRANSFERS_ANY = [
    {
        "id": 1,
        "transfer_type": TransferType.IN_TRANSFER,
        "amount": 1300.00,
        "receipt_id": 1,
        "from_": "Burger King",
        "to_": "me",
        "descr": ""
    },
    {
        "id": 2,
        "transfer_type": TransferType.IN_TRANSFER,
        "amount": 4800.00,
        "receipt_id": 2,
        "from_": "NSA",
        "to_": "me",
        "descr": ""
    },
    {
        "id": 3,
        "transfer_type": TransferType.OUT_TRANSFER,
        "amount": 800.00,
        "receipt_id": 3,
        "from_": "me",
        "to_": "they",
        "descr": "stuff"
    }
]


def simulate_receipts():
    rec1 = ReceiptSearch(id=1, amount=1300.00, net_amount=1000, client="Burger King", worker="me",
                         descr="data analysis")
    rec2 = ReceiptSearch(id=2, amount=2200, client="Biedronka", worker="me", descr="app")
    rec3 = ReceiptSearch(id=3, amount=390, client="me", vat_percentage=30, worker="Allegro",
                         descr="for hard_drive")
    return [rec1, rec2, rec3]


RECEIPTS = simulate_receipts()


def simulate_transfers():
    rec1, rec2, rec3 = RECEIPTS
    t1 = TransferSearch(
        id=1,
        transfer_type=TransferType.IN_TRANSFER,
        receipt_id=1,
        amount=1300.00,
        from_="Burger Queen",
        to_="me",
        descr="data analysis",
    )
    print(t1)
    t2 = TransferSearch(
        id=2,
        transfer_type=TransferType.IN_TRANSFER,
        receipt_id=2,
        amount=2200.00,
        from_="Biedronka",
        to_="me",
        descr="",
    )
    t3 = TransferSearch(
        id=3,
        transfer_type=TransferType.OUT_TRANSFER,
        receipt_id=3,
        to_="Allegro",
        from_="me",
        amount=390
    )
    tr_arr = [t1, t2, t3]

    return tr_arr


TRANSFERS = simulate_transfers()
