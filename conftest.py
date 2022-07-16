"""Define fixtures for tests."""
import pytest

from model import DefaultVatInvoice, NoVatInvoice, Transfer, TransferType


@pytest.fixture(scope="session")
def default_vat_invoice1():
    return DefaultVatInvoice(
        amount=600, client="Burger King", worker="me", descr="data analysis"
    )


@pytest.fixture(scope="session")
def default_vat_invoice2():
    return DefaultVatInvoice(
        amount=300, client="me", worker="Allegro", descr="for hard_drive"
    )


@pytest.fixture(scope="session")
def no_vat_invoice():
    return NoVatInvoice(amount=2200, client="Biedronka", worker="me", descr="app")


@pytest.fixture()
def transfer_for_default_vat_invoice1(default_vat_invoice1):
    inv = default_vat_invoice1
    t = Transfer(
        TransferType.IN_TRANSFER,
        invoice=inv,
        amount=600.00,
        _from="Burger Queen",
        _to="me",
        descr="data analysis",
    )
    return t


@pytest.fixture
def transfer_for_default_vat_invoice2(default_vat_invoice2):
    inv = default_vat_invoice2
    t = Transfer(
        TransferType.OUT_TRANSFER, invoice=inv, _to="Allegro", _from="me", amount=300
    )
    return t


@pytest.fixture()
def transfer_for_no_vat_invoice(no_vat_invoice):
    inv = no_vat_invoice
    t = Transfer(
        TransferType.IN_TRANSFER,
        invoice=inv,
        amount=2200.00,
        _from="Burger King",
        _to="me",
        descr="gift",
    )
    return t
