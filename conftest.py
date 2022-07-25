"""Define fixtures for tests."""
import pytest

from pycountant.schemas import Receipt, Transfer, TransferType


@pytest.fixture(scope="session")
def receipt1():
    return Receipt(
        id=1, amount=600, vat_percentage=20, client="Burger King", worker="me", descr="data analysis"
    )


@pytest.fixture(scope="session")
def receipt2():
    return Receipt(
        id=2, amount=300, client="me", worker="Allegro", descr="for hard_drive"
    )


@pytest.fixture(scope="session")
def receipt3():
    return Receipt(id=3, amount=2200, client="Biedronka", worker="me", descr="app")


@pytest.fixture()
def transfer_for_receipt1(receipt1):
    rec = receipt1
    t = Transfer(
        id=1,
        transfer_type=TransferType.IN_TRANSFER,
        receipt=rec,
        amount=600.00,
        _from="Burger Queen",
        _to="me",
        descr="data analysis",
    )
    return t


@pytest.fixture
def transfer_for_receipt2(receipt2):
    rec = receipt2
    t = Transfer(id=2, transfer_type=TransferType.OUT_TRANSFER, receipt=rec, _to="Allegro", _from="me", amount=300)
    return t


@pytest.fixture()
def transfer_for_receipt3(receipt3):
    rec = receipt3
    t = Transfer(id=3, transfer_type=TransferType.IN_TRANSFER, receipt=rec, amount=2200.00, _from="Burger King",
                 _to="me", descr="gift")
    return t
