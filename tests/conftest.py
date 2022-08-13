import pytest
from typing import Generator

from fastapi.testclient import TestClient
from app.main import app
from app.api import deps

from pycountant.sample_data import TRANSFERS_ANY
from pycountant.model import Transfer
from pycountant.calculations import BalanceResults

from typing import List


def override_transfers() -> List[Transfer]:
    transfers = []
    for tr in TRANSFERS_ANY:
        new_transfer = Transfer(
            transfer_type=tr["transfer_type"],
            amount=tr["amount"],
            receipt_id=tr["receipt_id"],
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
        vat_balance=600.0,
        income_tax_30=0,
        profit=500,
    )


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as _client:
        app.dependency_overrides[deps.get_transfers] = override_transfers
        app.dependency_overrides[deps.get_balance] = override_balance
        yield _client
        app.dependency_overrides = {}
