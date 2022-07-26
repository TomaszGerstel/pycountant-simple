"""Define fixtures for tests."""
import pytest

from pycountant.schemas import Receipt, Transfer, TransferType


# receipt with net amount, without indicated vat percentage or vat value
@pytest.fixture(scope="session")
def receipt1():
    return Receipt(id=1, amount=130, net_amount=100, client="me", worker="worker_from_some_firm",
                   descr="for_some_shopping")


# receipt with vat percentage
@pytest.fixture(scope="session")
def receipt2():
    return Receipt(id=2, amount=650.00, vat_percentage=30, client="client2_on_Invoice",
                   worker="worker_on_invoice", descr="descr")


# receipt with vat value, without indicated vat percentage or net amount
@pytest.fixture(scope="session")
def receipt3():
    return Receipt(id=3, amount=260, vat_value=60, client="client1", worker="me",
                   descr="example_descr")


# out transfer without optional values
@pytest.fixture()
def transfer_for_receipt1(receipt1):
    rec = receipt1
    t = Transfer(id=1, receipt=rec, amount=130, transfer_type=TransferType.OUT_TRANSFER)
    return t


# transfer without amount, taking amount from invoice
@pytest.fixture
def transfer_for_receipt2(receipt2):
    rec = receipt2
    t = Transfer(id=2, receipt=rec, _from="client2", _to="me", descr="example_desc",
                 transfer_type=TransferType.IN_TRANSFER)
    return t


@pytest.fixture()
def transfer_for_receipt3(receipt3):
    rec = receipt3
    t = Transfer(id=3, receipt=rec, amount=260, _from="client1", _to="me", descr="example_desc",
                 transfer_type=TransferType.IN_TRANSFER)
    return t


# transfer with negative value
# @pytest.fixture()
# def transfer4():
#     t = Transfer(id=4, receipt=receipt1, amount=-650, transfer_type=TransferType.OUT_TRANSFER)
#     return t
