"""testing knowing values from receipts and transfers defined in conftest.py file"""
import pytest

from pycountant.calculations import calculate_balance
from pycountant.exceptions import NegativeValueError


def test_example_transfers_balance(
    receipt1,
    receipt2,
    receipt3,
    receipt4,
    transfer_for_receipt1,
    transfer_for_receipt2,
    transfer_for_receipt3,
    transfer4,
    transfer5,
    transfer6,
    transfer7
):

    # Given
    rec1, rec2, rec3, rec4 = receipt1, receipt2, receipt3, receipt4
    tr1 = transfer_for_receipt1
    tr2 = transfer_for_receipt2
    tr3 = transfer_for_receipt3
    tr4 = transfer4
    tr5 = transfer5
    tr6 = transfer6
    tr7 = transfer7

    tr_arr1 = [tr1, tr2, tr3, tr5, tr6, tr7]
    tr_arr2 = [tr4]
    rec_arr1 = [rec1, rec2, rec3]
    rec_arr2 = [rec4]

    # When
    balance = calculate_balance(tr_arr1, rec_arr1)

    # Then
    # 650 + 260(in transfers) - 130(out transfer) - 200(salary)
    # - 100(vat paid) - 80(tax paid to tax office) = 400
    assert balance.balance == 400.0
    # 130 out transfer
    assert balance.costs == 130.0
    # 650 + 260 in transfers = 910
    assert balance.gross_income == 910.0
    # 650 in with 30% vat + 260 wit 30% vat - 130 with 30% out transfer
    # = 500 + 200 - 100 = 600
    assert balance.net_balance == 600.0
    # 30% vat from 650 in transfer + 30% from 260
    # - 30% vat from 130 out transfer = 180
    assert balance.due_vat == 180.0
    # 30% income tax from 500 + 200 net value in transfer
    # - 100 net value out transfer = 180
    assert balance.due_tax_30 == 180.0
    # net balance (600) - income tax to pay (180) equals 420
    assert balance.due_profit == 420.0
    # paid profit: one salary transfer with 200
    assert balance.paid_profit == 200.0
    # remaining profit: due profit - paid profit: 420 - 200 = 220
    assert balance.remaining_profit == 220.0
    # paid vat: one transfer with 100
    assert balance.paid_vat == 100.0
    # vat balance: due vat - paid vat: 180 - 100 = 80
    assert balance.vat_balance == 80.0
    # paid tax: one transfer with 80
    assert balance.paid_tax == 80.0
    # income ta 30 balance: due tax - paid tax: 180 - 80 = 100
    assert balance.income_tax_30 == 100
    # other costs: paid profit, vat and tax: 200 + 100 + 80 == 380
    assert balance.other_costs == 380
    # try to make calculations for transaction with negative value
    with pytest.raises(NegativeValueError):
        balance2 = calculate_balance(tr_arr2, rec_arr2)
