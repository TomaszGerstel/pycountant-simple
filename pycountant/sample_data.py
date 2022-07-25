from pycountant.schemas import Receipt, Transfer, TransferType


# Simulate database
RECEIPTS_ANY = [
    {
        "id": 1,
        "amount": 1500.0,
        "client": "Burger King",
        "worker": "me",
        "descr": "data analysis",
    },
    {
        "id": 2,
        "amount": 5000.0,
        "client": "NSA",
        "worker": "me",
        "descr": "secret data wrangling",
        "vat_percentage": 0,
    },
]


TRANSFERS_ANY = [
    {
        "id": 1,
        "transfer_type": TransferType.IN_TRANSFER,
        "amount": 1300.00,
        "vat_percentage": 30,
        "invoice_id": 1,
        "_from": "Burger King",
        "_to": "me",
    },
    {
        "id": 2,
        "transfer_type": TransferType.IN_TRANSFER,
        "amount": 5000.00,
        "vat_percentage": 30,
        "invoice_id": 2,
        "_from": "NSA",
        "_to": "me",
    },
]


def simulate_receipts():
    inv1 = Receipt(
        amount=1300.00, net_amount=1000, client="Burger King", worker="me", descr="data analysis"
    )
    inv2 = Receipt(amount=2200, client="Biedronka", worker="me", descr="app")
    inv3 = Receipt(amount=390, client="me", vat_percent=30, worker="Allegro",
                   descr="for hard_drive")
    return [inv1, inv2, inv3]


RECEIPTS = simulate_receipts()


def simulate_transfers():
    rec1, rec2, rec3 = RECEIPTS
    t1 = Transfer(
        TransferType.IN_TRANSFER,
        receipt=rec1,
        amount=1300.00,
        _from="Burger Queen",
        _to="me",
        descr="data analysis",
    )
    print(t1)
    t2 = Transfer(
        TransferType.IN_TRANSFER,
        receipt=rec2,
        amount=2200.00,
        _from="Burger King",
        _to="me",
        descr="gift",
    )
    t3 = Transfer(
        TransferType.OUT_TRANSFER,
        receipt=rec3,
        _to="Allegro",
        _from="me",
        amount=390
    )
    tr_arr = [t1, t2, t3]

    return tr_arr


TRANSFERS = simulate_transfers()
