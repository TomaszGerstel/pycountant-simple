from pycountant.calculations import calculate_balance


def test_example_receipt_balance(
    receipt1, transfer_for_receipt1
):
    # Given
    inv = receipt1
    tr = transfer_for_receipt1
    tr_arr = [tr]

    # When
    balance = calculate_balance(tr_arr)

    # Then
    print(balance)
    assert balance.gross_income == 600.0
    assert balance.balance == 600.0
    assert balance.net_balance == 500.0
    assert balance.vat_balance == 100.0
    assert balance.income_tax_30 == 150.0
    assert balance.profit == 350.0
