from pycountant.calculations import BalanceOfFinances
from pycountant.schemas import (
    Receipt,
    TransferType,
    Transfer,
)


class TestExampleStories:
    """
    Testing example stories from file stories.md
    """
    # Unit tests to story 1. from stories.md file
    # Receipt with set fixed vat = 20%
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
