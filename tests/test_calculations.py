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
    assert balance.vat_due == 180.0
    # 19% income tax from 500 + 200 net value in transfer
    # - 100 net value out transfer = 114
    assert balance.flat_tax_due == 114.0
    # lump sum tax for gross income is: 12% (default rate) from 910 -> 109.2
    assert balance.lump_sum_tax_due == 109.2
    # net balance (600) - income tax to pay (180) equals 486
    assert balance.profit_due_flat == 486.0
    # net balance (600) - lump-sum tax to pay (109.2) equals 490.8
    assert balance.profit_due_lump == 490.8
    # paid profit: one salary transfer with 200
    assert balance.profit_paid == 200.0
    # remaining profit: due profit flat - paid profit: 486 - 200 = 286
    assert balance.profit_remaining_flat == 286.0
    # remaining profit: due profit lump - paid profit: 490.8 - 200 = 290.8
    assert balance.profit_remaining_lump == 290.8
    # paid vat: one transfer with 100
    assert balance.vat_paid == 100.0
    # vat balance: due vat - paid vat: 180 - 100 = 80
    assert balance.vat_balance == 80.0
    # paid tax: one transfer with 80
    assert balance.tax_paid == 80.0
    # income tax 19 balance: due tax - paid tax: 114 - 80 = 34
    assert balance.flat_tax_balance == 34
    # lump-sum tax balance: due lump-sum tax - paid tax = 29.2
    assert balance.lump_sum_tax_balance == 29.2
    # other costs: paid profit, vat and tax: 200 + 100 + 80 == 380
    assert balance.other_costs == 380
    # try to make calculations for transaction with negative value
    with pytest.raises(NegativeValueError):
        balance2 = calculate_balance(tr_arr2, rec_arr2)
