from calculations import BalanceOfFinances


def test_default_vat_invoice_balance(
    default_vat_invoice1, transfer_for_default_vat_invoice1
):
    # Given
    inv = default_vat_invoice1
    tr = transfer_for_default_vat_invoice1
    tr_arr = [tr]

    # When
    balance = BalanceOfFinances(tr_arr)

    # Then
    print(balance)
    assert balance.gross_income == 600.0
    assert balance.balance == 600.0
    assert balance.net_balance == 500.0
    assert balance.vat_balance == 100.0
    assert balance.income_tax_30 == 150.0
    assert balance.profit == 350.0
