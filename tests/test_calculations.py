"""testing knowing values from receipts and transfers defined in conftest.py file"""
import pytest

from pycountant.calculations import calculate_balance
from pycountant.exceptions import NegativeValueError


def test_example_transfers_balance(
    transfers_and_receipts_good_values,
):
    # Given
    tr_arr1, rec_arr1, balance_expected = transfers_and_receipts_good_values

    # When
    balance = calculate_balance(tr_arr1, rec_arr1)

    # Then
    assert balance == balance_expected


def test_example_transfers_balance_negative_value_error(
    transfers_and_receipts_negative_value,
):
    # Given
    tr_arr2, rec_arr2 = transfers_and_receipts_negative_value

    # Then
    # try to make calculations for transaction with negative value
    with pytest.raises(NegativeValueError):
        balance2 = calculate_balance(tr_arr2, rec_arr2)