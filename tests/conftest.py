import pytest
from typing import Generator

from fastapi.testclient import TestClient
from app.main import app
from app.api import deps

from pycountant.sample_data import TRANSFERS_ANY
from pycountant.model import Transfer
from pycountant.calculations import BalanceResults

from typing import List


# not used?
def override_transfers() -> List[Transfer]:
    transfers = []
    for tr in TRANSFERS_ANY:
        new_transfer = Transfer(
            transfer_type=tr["transfer_type"],
            amount=tr["amount"],
            receipt_id=tr["receipt_id"],
            date=tr["date"],
            from_=tr["from_"],
            to_=tr["to_"],
            descr=tr["descr"],
        )
        transfers.append(new_transfer)
    return transfers


def override_balance() -> BalanceResults:
    return BalanceResults(
        costs=100.0,
        gross_income=1000.0,
        balance=900.0,
        net_balance=750.0,
        vat_due=600.0,
        flat_tax_due=0,
        profit_due_flat=500,
    )


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as _client:
        app.dependency_overrides[deps.get_transfers] = override_transfers
        app.dependency_overrides[deps.get_balance] = override_balance
        yield _client
        app.dependency_overrides = {}


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


# salary paid
@pytest.fixture()
def transfer5():
    t = TransferSearch(
        id=5,
        # receipt_id=None,
        amount=200,
        date="2022-09-05",
        user_id=1,
        transfer_type=TransferType.SALARY
    )
    return t


# vat paid to treasury
@pytest.fixture()
def transfer6():
    t = TransferSearch(
        id=6,
        # receipt_id=None,
        amount=100,
        date="2022-09-05",
        user_id=1,
        transfer_type=TransferType.VAT_OUT_TRANSFER
    )
    return t


# tax paid to tax office
@pytest.fixture()
def transfer7():
    t = TransferSearch(
        id=7,
        # receipt_id=None,
        amount=80,
        date="2022-09-05",
        user_id=1,
        transfer_type=TransferType.TAX_OUT_TRANSFER
    )
    return t


@pytest.fixture
def transfers_and_receipts_good_values(
    receipt1,
    receipt2,
    receipt3,
    transfer_for_receipt1,
    transfer_for_receipt2,
    transfer_for_receipt3,
    transfer5,
    transfer6,
    transfer7
):
    rec1, rec2, rec3 = receipt1, receipt2, receipt3
    tr1 = transfer_for_receipt1
    tr2 = transfer_for_receipt2
    tr3 = transfer_for_receipt3
    tr5 = transfer5
    tr6 = transfer6
    tr7 = transfer7

    tr_arr1 = [tr1, tr2, tr3, tr5, tr6, tr7]
    rec_arr1 = [rec1, rec2, rec3]
    default_lump_tax_rate = 12  # be careful if this changes
    balance_expected = BalanceResults(
        balance=400.0,
        costs=100.0,
        gross_income=700,
        net_balance=600.0,  # TODO: rename it to gross revenue
        vat_due=180.0,
        flat_tax_due=114.0,
        lump_sum_tax_due=84,
        lump_tax_rate=default_lump_tax_rate,
        profit_due_flat=486.0,
        profit_due_lump=516.0,
        profit_paid=200.0,
        profit_remaining_flat=286.0,
        profit_remaining_lump=316.0,
        vat_paid=100.0,
        vat_balance=80.0,
        tax_paid=80.0,
        flat_tax_balance=34,
        lump_sum_tax_balance=4,
        other_costs=380,
    )
    # Explanation
    # -----------
    # * balance: 650 + 260(in transfers) - 130(out transfer) - 200(salary)
    #            - 100(vat paid) - 80(tax paid to tax office) = 400
    # * costs: 100 out transfer
    # * gross income: 700
    # * net balance (RENAME->gross revenue): gross income - costs = 700 - 100 = 600
    # * vat due: 30% vat from 650 in transfer + 30% from 260
    #            - 30% vat from 130 out transfer = 180
    # * flat tax due: 19% income tax from gross revenue = 500 + 200 net value in transfer
    #                 - 100 net value out transfer = 114
    # * lump sum tax due:  for gross income is: 12% (default rate) from gross income -> 84
    # * profit due if flat: net balance (600) - income tax to pay (180) equals 486
    # * profit due if lump: net balance (600) - lump-sum tax to pay (84) equals 516
    # * paid profit: one salary transfer with 200
    # * remaining profit if flat tax: due profit flat - paid profit: 486 - 200 = 286
    # * remaining profit if lump-sum tax: due profit lump - paid profit: 516 - 200 = 316
    # * paid vat: one transfer with 100
    # * vat balance: due vat - paid vat: 180 - 100 = 80
    # * paid tax: one transfer with 80
    # * flat tax balance: due tax - paid tax: 114 - 80 = 34
    # * lump-sum tax balance: due lump-sum tax - paid tax = 84 - 80 = 4
    # * other costs: paid profit, vat and tax: 200 + 100 + 80 == 380
    return tr_arr1, rec_arr1, balance_expected


@pytest.fixture
def transfers_and_receipts_negative_value(transfer4, receipt4):
    tr_arr2 = [transfer4]
    rec_arr2 = [receipt4]
    return tr_arr2, rec_arr2