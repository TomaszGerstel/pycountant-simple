"""Define fixtures for tests."""
import pytest

from pycountant.schemas import ReceiptSearch, TransferSearch, TransferType


# receipt with net amount, without indicated vat percentage or vat value
@pytest.fixture(scope="session")
def receipt1():
    return ReceiptSearch(
        id=1,
        amount=130,
        net_amount=100,
        client="me",
        date="2022-09-01",
        user_id=1,
        worker="worker_from_some_firm",
        descr="for_some_shopping",
    )


# receipt with vat percentage
@pytest.fixture(scope="session")
def receipt2():
    return ReceiptSearch(
        id=2,
        amount=650.00,
        vat_percentage=30,
        date="2022-09-02",
        user_id=1,
        client="client2_on_Invoice",
        worker="worker_on_invoice",
        descr="descr",
    )


# receipt with vat value, without indicated vat percentage or net amount
@pytest.fixture(scope="session")
def receipt3():
    return ReceiptSearch(
        id=3,
        amount=260,
        vat_value=60,
        date="2022-09-03",
        user_id=1,
        client="client1",
        worker="me",
        descr="example_descr",
    )


# receipt with negative amount
@pytest.fixture(scope="session")
def receipt4():
    return ReceiptSearch(
        id=4,
        amount=-650,
        vat_value=150,
        date="2022-09-01",
        user_id=1,
        client="client4",
        worker="me",
        descr="example_descr",
    )


# out transfer without optional values
@pytest.fixture()
def transfer_for_receipt1(receipt1):
    rec = receipt1
    t = TransferSearch(
        id=1,
        receipt_id=1,
        amount=130,
        date="2022-09-01",
        user_id=1,
        transfer_type=TransferType.OUT_TRANSFER
    )
    return t


# transfer without amount, taking amount from invoice
@pytest.fixture
def transfer_for_receipt2(receipt2):
    rec = receipt2
    t = TransferSearch(
        id=2,
        receipt_id=2,
        date="2022-09-02",
        user_id=1,
        _from="client2",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    return t


@pytest.fixture()
def transfer_for_receipt3(receipt3):
    rec = receipt3
    t = TransferSearch(
        id=3,
        receipt_id=3,
        amount=260,
        date="2022-09-03",
        user_id=1,
        _from="client1",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    return t


# transfer with negative value
@pytest.fixture()
def transfer4(receipt4):
    rec = receipt4
    t = TransferSearch(
        id=4,
        receipt_id=4,
        amount=-650,
        date="2022-09-01",
        user_id=1,
        transfer_type=TransferType.OUT_TRANSFER
    )
    return t
