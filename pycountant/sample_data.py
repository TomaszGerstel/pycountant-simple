from pycountant.model import DefaultVatInvoice, NoVatInvoice, Transfer, TransferType


# Simulate database
INVOICES_ANY = [
    {
        'id': 1,
        'amount': 1500.0,
        'client': "Burger King",
        'worker': "me",
        'descr': "data analysis",
    },
    {
        'id': 2,
        'amount': 5000.0,
        'client': "NSA",
        'worker': "me",
        'descr': "secret data wrangling",
        'vat_percentage': 0,
    },
]


TRANSFERS_ANY = [
    {
        'id': 1,
        'transfer_type': TransferType.IN_TRANSFER,
        'amount': 1500.00,
        'invoice_id': 1,
        '_from': "Burger King",
        '_to': 'me',
    },
    {
        'id': 2,
        'transfer_type': TransferType.IN_TRANSFER,
        'amount': 5000.00,
        'invoice_id': 2,
        '_from': "NSA",
        '_to': 'me',
    },
]


def simulate_invoices():
    inv1 = DefaultVatInvoice(
        amount=1500.00, client="Burger King", worker="me", descr="data analysis"
    )
    inv2 = NoVatInvoice(amount=2200, client="Biedronka", worker="me", descr="app")
    inv3 = DefaultVatInvoice(
        amount=300, client="me", worker="Allegro", descr="for hard_drive"
    )
    return [inv1, inv2, inv3]


INVOICES = simulate_invoices()
def simulate_transfers():
    inv1, inv2, inv3 = INVOICES
    t1 = Transfer(
        TransferType.IN_TRANSFER,
        invoice=inv1,
        amount=1500.00,
        _from="Burger Queen",
        _to="me",
        descr="data analysis",
    )
    print(t1)
    t2 = Transfer(
        TransferType.IN_TRANSFER,
        invoice=inv2,
        amount=2200.00,
        _from="Burger King",
        _to="me",
        descr="gift",
    )
    t3 = Transfer(
        TransferType.OUT_TRANSFER, invoice=inv3, _to="Allegro", _from="me", amount=300
    )
    tr_arr = [t1, t2, t3]

    return tr_arr


TRANSFERS = simulate_transfers()
