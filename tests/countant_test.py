import pycountant.exceptions
from pycountant.calculations import BalanceOfFinances
from pycountant.schemas import (
    Receipt,
    TransferType,
    Transfer,
)

import pytest


# @pytest.mark.xfail(reason="Updated VAT percentage")
class TestCountant:
    """receipt with net amount, without indicated vat percentage or vat value"""
    receipt1 = Receipt(
        id=1,
        amount=130,
        net_amount=100,
        client="me",
        worker="worker_from_some_firm",
        descr="for_some_shopping",
    )
    """receipt vat percentage"""
    receipt2 = Receipt(
        id=2,
        amount=650.00,
        vat_percentage=30,
        client="client2_on_Invoice",
        worker="worker_on_invoice",
        descr="descr",
    )
    """receipt vat value, without indicated vat percentage or net amount"""
    receipt3 = Receipt(
        id=3,
        amount=260,
        vat_value=60,
        client="client1",
        worker="me",
        descr="example_descr"
    )

    """out transfer without optional values"""
    transfer1 = Transfer(
        id=1, receipt=receipt1, amount=130, transfer_type=TransferType.OUT_TRANSFER
    )
    """transfer without amount, taking amount from invoice"""
    transfer2 = Transfer(
        id=2,
        receipt=receipt2,
        _from="client2",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    transfer3 = Transfer(
        id=3,
        receipt=receipt3,
        amount=260,
        _from="client1",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    """transfer with negative value"""
    transfer4 = Transfer(id=4, amount=-650, transfer_type=TransferType.OUT_TRANSFER)
    """list of transfers"""
    transfers_list = [transfer1, transfer2, transfer3]
    """list with wrong transfer4"""
    transfers_list2 = [transfer1, transfer3, transfer4]

    balance = BalanceOfFinances(transfers_list)

    def test_methods_from_balance_finances_should_return_known_gross_balance(self):
        """650+260(in transfers)-130(out transfer)=780"""
        result = self.balance.balance
        assert result == 780

    def test_methods_from_balance_finances_should_return_known_costs(self):
        """130 out transfer"""
        result = self.balance.costs
        assert result == 130

    def test_methods_from_balance_finances_should_return_known_gross_income(self):
        """650+260 in transfers=910"""
        result = self.balance.gross_income
        assert result == 910

    def test_methods_from_amount_balance_should_return_known_net_balance(self):
        """650 in with 30% vat + 260 wit 30% vat - 130 with 30% out transfer
        = 500 + 200 - 100 = 600 (round)"""
        result = self.balance.net_balance
        assert result == 600

    def test_methods_from_amount_balance_should_return_known_vat_balance(self):
        """30% vat from 650 in transfer + 30% from 260 - 30% vat from 130 out transfer = 180"""
        result = self.balance.vat_balance
        assert result == 180

    def test_methods_from_amount_balance_should_return_known_income_tax(self):
        """30% income tax from 500+200 net value in transfer-100 net value out transfer = 180"""
        result = self.balance.income_tax_30
        assert result == 180

    def test_methods_from_amount_balance_should_return_known_profit(self):
        """net balance (600) - income tax to pay (180) equals 420"""
        result = self.balance.profit
        assert result == 420

    # single object test of methods, not null tests?
    # exception tests, negative value


class TestExampleStories:
    """Unit tests to story 1. from stories.md file"""

    """Receipt with set fixed vat = 20%"""
    rec1 = Receipt(
        id=1,
        amount=600,
        vat_percentage=20,
        worker="me",
        client="Masterkelm",
        descr="for service",
    )

    """Incoming transfer with above receipt"""
    transfer1 = Transfer(id=1, transfer_type=TransferType.IN_TRANSFER, receipt=rec1)

    """passing the transfer object to the calculations object"""
    arr1 = [transfer1]
    balance1 = BalanceOfFinances(arr1)

    def test_balance_calc_for_example_story_01(self):
        """gross income is 600"""
        assert self.balance1.gross_income == 600
        """balance is 600 (with expenses = 0)"""
        assert self.balance1.balance == 600
        """vat balance: 500 + 20% vat is amount = 600 >> vat = 100.
        have to pay to the treasury"""
        assert self.balance1.vat_balance == 100
        """net balance: 600 - vat 20% = 500"""
        assert self.balance1.net_balance == 500
        """income tax 30% from 500 (amount without vat) is 150.
        have to pay to tax office"""
        assert self.balance1.income_tax_30 == 150
        """profit: 70% from net income (500) = 350
        and can be transfer to personal bank account"""
        assert self.balance1.profit == 350
        """there was no expense, it should return 0"""
        assert self.balance1.costs == 0

    """Testing story 2. from stories.md"""

    """receipt to transfer to pay costs for platform"""
    rec2 = Receipt(id=2, amount=60, vat_percentage=20, client="me", worker="freelance_platform", descr="profit")
    transfer2 = Transfer(id=2, transfer_type=TransferType.OUT_TRANSFER, receipt=rec2, amount=60)
    """list included transfer from story 1. and above expense"""
    arr2 = [transfer1, transfer2]
    balance2 = BalanceOfFinances(arr2)

    def test_balance_calc_for_example_story_02(self):
        """600(500 with 20% vat) in and 60(50 with 20% vat) out transfer = 100-10 >> vat = 90.
        have to pay to the treasury."""
        assert self.balance2.vat_balance == 90
        """have to pay income tax (gross income - costs (VARIANT B))
        500 EUR - 50 = 450 tax base > 30% of 450 = 135"""
        assert self.balance2.income_tax_30 == 135
        """50 EUR + 10 EUR VAT is as costs (one outgoing transfer)"""
        assert self.balance2.costs == 60
        """what's left (net amount(500-50 is 450) minus 30% income tax(135) = 315) 
        is profit and can be get as salary"""
        assert self.balance2.profit == 315

    """Testing story 3. from stories.md"""

    """ticket/hotel - reimbursement transfer to personal account 500 EUR"""
    rec3 = Receipt(id=3, amount=500, client="me", worker="Ryan Air", descr="ticket")
    transfer3 = Transfer(id=3, transfer_type=TransferType.OUT_TRANSFER, receipt=rec3, amount=500)
    """list included transfer from story 1, 2 and above reimbursement"""
    arr3 = [transfer1, transfer2, transfer3]
    balance3 = BalanceOfFinances(arr3)

    def test_balance_calc_for_example_story_03(self):
        """now costs are 60+500 for ticket -> 560"""
        assert self.balance3.costs == 560
        """and balance is 600-60-500 -> 40"""
        assert self.balance3.balance == 40

    """Unit tests to story 4. from stories.md file"""

    """Receipt without set vat (default vat percentage is 0)"""
    rec4 = Receipt(id=4, amount=500, worker="me", client="Masterkelm", descr="for service")

    """Incoming transfer with above receipt"""
    transfer4 = Transfer(id=4, transfer_type=TransferType.IN_TRANSFER, receipt=rec4)

    """passing the transfer object to the calculations object"""
    arr4 = [transfer4]
    balance4 = BalanceOfFinances(arr4)

    def test_balance_calc_for_example_story_04(self):
        """gross income is 500"""
        assert self.balance4.gross_income == 500
        """balance is 600 (with expenses = 0)"""
        assert self.balance4.balance == 500
        """vat balance: 500 + 0% vat is amount = 500 >> vat = 0"""
        assert self.balance4.vat_balance == 0
        """net balance: without vat equals gross income = 500"""
        assert self.balance4.net_balance == 500
        """income tax 30% from 500 (amount without vat) is 150.
        have to pay to tax office"""
        assert self.balance4.income_tax_30 == 150
        """profit: 70% from net income (500) = 350
        and can be transfer to personal bank account"""
        assert self.balance4.profit == 350
        """there was no expense, it should return 0"""
        assert self.balance4.costs == 0

    """Unit tests to story 4 + 2. from stories.md file"""

    """adding transfers from stories 2 and 4"""
    arr6 = [transfer2, transfer4]
    balance6 = BalanceOfFinances(arr6)

    def test_balance_calc_for_example_story_06(self):
        """gross income is 500"""
        assert self.balance6.gross_income == 500
        """balance is 600 (with expenses = 60)"""
        assert self.balance6.balance == 440
        """vat balance: 0% from 500 - 20% from 60 -> vat = -10
        you paid 10 EUR more vat than you should to treasury """
        assert self.balance6.vat_balance == -10
        """net balance: without vat equals gross income = 500-50"""
        assert self.balance6.net_balance == 450
        """income tax 30% from 450 (amount without vat) is 135.
        have to pay to tax office"""
        assert self.balance6.income_tax_30 == 135
        """profit: 70% from net income (450) = 325
        and can be transfer to personal bank account"""
        assert self.balance6.profit == 315
        """there was one expense for 60"""
        assert self.balance6.costs == 60
