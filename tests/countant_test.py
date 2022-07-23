import pycountant.exceptions
from pycountant.calculations import BalanceOfFinances
from pycountant.model import (
    Receipt,
    TransferType,
    Transfer,
    )

import pytest


# @pytest.mark.xfail(reason="Updated VAT percentage")
class TestCountant:
    """receipt with net amount, without indicated vat percentage or vat value"""
    receipt1 = Receipt(
        amount=130,
        net_amount=100,
        client="me",
        worker="worker_from_some_firm",
        descr="for_some_shopping",
    )
    """receipt vat percentage"""
    receipt2 = Receipt(
        amount=650.00,
        vat_percent=30,
        client="client2_on_Invoice",
        worker="worker_on_invoice",
        descr="descr",
    )
    """receipt vat value, without indicated vat percentage or net amount"""
    receipt3 = Receipt(
        amount=260,
        vat_value=60,
        client="client1",
        worker="me",
        descr="example_descr"
    )

    """out transfer without optional values"""
    transfer1 = Transfer(
        receipt=receipt1, amount=130, transfer_type=TransferType.OUT_TRANSFER
    )
    """transfer without amount, taking amount from invoice"""
    transfer2 = Transfer(
        receipt=receipt2,
        _from="client2",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    transfer3 = Transfer(
        receipt=receipt3,
        amount=260,
        _from="client1",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    """transfer with negative value"""
    transfer4 = Transfer(amount=-650, transfer_type=TransferType.OUT_TRANSFER)
    """list of transfers"""
    transfers_list = [transfer1, transfer2, transfer3]
    """list with wrong transfer4"""
    transfers_list2 = [transfer1, transfer3, transfer4]

    balance = BalanceOfFinances(transfers_list)

    def test_methods_from_balance_finances_should_return_known_gross_balance(self):
        """650+260(in transfers)-130(out transfer)=780"""
        result = self.balance.balance
        assert result == 780

    # to add: get costs, gross income,

    def test_methods_from_amount_balance_should_return_known_net_balance(self):
        """650 in with 30% vat + 260 wit 30% vat - 130 with 30% out transfer
        = 500 + 200 - 100 = 600 (round)"""
        result = self.balance.net_balance
        assert result == 600

    def test_methods_from_amount_balance_should_return_known_vat_balance(self):
        """30% vat from 650 in transfer + 30% from 260 - 30% vat from 130 out transfer = 180"""
        result = self.balance.vat_balance
        assert result == 180

        # to add: income tax, profit

    # single object test of methods, not null tests?
    # test stories
    # exception tests, negative value


class TestExampleStories:

    """Got 600 EUR transfer for a European invoice (500 EUR gros; 20% * 500 EUR = 100 EUR VAT)
    -> 100 EUR VAT --> pay to the treasury -> 30% x 500 EUR of income tax
    --> pay to the tax office (different transfer destination than VAT)
    -> 70% x 500 EUR of income net --> transfer to my personal bank account"""

    """Invoice with set fixed vat = 20%"""
    rec1 = Receipt(
        amount=600,
        vat_percent=20,
        worker="me",
        client="Masterkelm",
        descr="for service",
    )

    """Incoming transfer with above invoice"""
    transfer1 = Transfer(TransferType.IN_TRANSFER, receipt=rec1)

    """passing the transfer object to the calculations object"""
    arr1 = [transfer1]
    balance1 = BalanceOfFinances(arr1)

    def test_gross_income_calc(self):
        """income is 600"""
        assert self.balance1.gross_income == 600

    def test_balance_calc(self):
        """balance is 600 (with expenses = 0)"""
        assert self.balance1.balance == 600

    def test_vat_balance_calc(self):
        """500 + 20% vat is amount = 600 >> vat = 100.
        have to pay to the treasury"""
        assert self.balance1.vat_balance == 100

    def test_net_balance_calc(self):
        """600 - vat 20% = 500"""
        assert self.balance1.net_balance == 500

    def test_calc_income_tax(self):
        """income tax 30% from 500 (amount without vat) is 150.
        have to pay to tax office"""
        assert self.balance1.income_tax_30 == 150

    def test_profit_calc(self):
        """70% from net income (500) = 350
        and can be transfer to personal bank account"""
        assert self.balance1.profit == 350

    def test_costs_calc(self):
        """there was no expense, it should return 0"""
        assert self.balance1.costs == 0
