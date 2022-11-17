from pycountant.calculations import calculate_balance
from pycountant.schemas import ReceiptSearch, TransferType, TransferSearch


class TestExampleStories:
    """
    Testing example stories from file stories.md
    """

    # Unit tests to story 1. from stories.md file

    # Receipt with set fixed vat = 20%
    rec1 = ReceiptSearch(
        id=1,
        amount=600,
        vat_percentage=20,
        date="2022-09-01",
        user_id=1,
        worker="me",
        client="Masterkelm",
        descr="for service",
    )
    # Incoming transfer with above receipt
    transfer1 = TransferSearch(
        id=1,
        receipt_id=1,
        date="2022-09-01",
        user_id=1,
        transfer_type=TransferType.IN_TRANSFER
    )
    # passing the transfer object to the calculations object
    tArr1 = [transfer1]
    rArr1 = [rec1]
    balance1 = calculate_balance(tArr1, rArr1)

    def test_balance_calc_for_example_story_01(self):
        # gross income is 600
        assert self.balance1.gross_income == 600
        # balance is 600 (with expenses = 0)
        assert self.balance1.balance == 600
        # vat balance: 500 + 20% vat is amount = 600 >> vat = 100.
        # have to pay to the treasury
        assert self.balance1.vat_due == 100
        # net balance: 600 - vat 20% = 500
        assert self.balance1.net_balance == 500
        # income tax 19% from 500 (amount without vat) is 95.
        # have to pay to tax office
        assert self.balance1.flat_tax_due == 95
        # profit: 81% from net income (500) = 405
        # and can be transfer to personal bank account
        assert self.balance1.profit_due == 405
        # there was no expense, it should return 0
        assert self.balance1.costs == 0

    # Testing story 2. from stories.md

    # receipt to transfer to pay costs for platform
    rec2 = ReceiptSearch(
        id=2,
        amount=60,
        vat_percentage=20,
        date="2022-09-02",
        user_id=1,
        client="me",
        worker="freelance_platform",
        descr="profit",
    )
    transfer2 = TransferSearch(
        id=2,
        transfer_type=TransferType.OUT_TRANSFER,
        date="2022-09-02",
        user_id=1,
        receipt_id=2,
        amount=60
    )
    # list included transfer from story 1. and above expense
    tArr2 = [transfer1, transfer2]
    rArr2 = [rec1, rec2]
    balance2 = calculate_balance(tArr2, rArr2)

    def test_balance_calc_for_example_story_02(self):
        # 600(500 with 20% vat) in and 60(50 with 20% vat) out transfer = 100-10 >> vat = 90.
        # have to pay to the treasury.
        assert self.balance2.vat_due == 90
        # have to pay income tax (gross income - costs (VARIANT B))
        # 500 EUR - 50 = 450 tax base -> 19% of 450 = 85.5
        assert self.balance2.flat_tax_due == 85.5
        # 50 EUR + 10 EUR VAT is as costs (one outgoing transfer)
        assert self.balance2.costs == 60
        # what's left (net amount(500-50 is 450) minus 19% income tax(85.5) = 364.5)
        # is profit and can be get as salary
        assert self.balance2.profit_due == 364.5

    # Testing story 3. from stories.md

    # ticket/hotel - reimbursement tansfer to personal account 500 EUR
    rec3 = ReceiptSearch(
        id=3,
        amount=500,
        date="2022-09-03",
        user_id=1,
        client="me",
        worker="Ryan Air",
        descr="ticket"
    )
    transfer3 = TransferSearch(
        id=3,
        transfer_type=TransferType.OUT_TRANSFER,
        receipt_id=3,
        amount=500,
        date="2022-09-03",
        user_id=1
    )
    # list included transfer from story 1, 2 and above reimbursement
    tArr3 = [transfer1, transfer2, transfer3]
    rArr3 = [rec1, rec2, rec3]
    balance3 = calculate_balance(tArr3, rArr3)

    def test_balance_calc_for_example_story_03(self):
        # now costs are 60+500 for ticket -> 560
        assert self.balance3.costs == 560
        # and balance is 600-60-500 -> 40
        assert self.balance3.balance == 40

    # Unit tests to story 4. from stories.md file

    # Receipt without set vat (default vat percentage is 0)
    rec4 = ReceiptSearch(
        id=4,
        amount=500,
        date="2022-09-04",
        user_id=1,
        worker="me",
        client="Masterkelm",
        descr="for service"
    )

    # Incoming transfer with above receipt
    transfer4 = TransferSearch(
        id=4,
        transfer_type=TransferType.IN_TRANSFER,
        receipt_id=4,
        date="2022-09-04",
        user_id=1
    )

    # passing the transfer object to the calculations object
    tArr4 = [transfer4]
    rArr4 = [rec4]
    balance4 = calculate_balance(tArr4, rArr4)

    def test_balance_calc_for_example_story_04(self):
        # gross income is 500
        assert self.balance4.gross_income == 500
        # balance is 500 (with expenses = 0)
        assert self.balance4.balance == 500
        # vat balance: 500 + 0% vat is amount = 500 >> vat = 0
        assert self.balance4.vat_due == 0
        # net balance: without vat equals gross income = 500
        assert self.balance4.net_balance == 500
        # income tax 19% from 500 (amount without vat) is 95.
        # have to pay to tax office
        assert self.balance4.flat_tax_due == 95
        # profit: 81% from net income (500) = 405
        # and can be transfer to personal bank account
        assert self.balance4.profit_due == 405
        # there was no expense, it should return 0
        assert self.balance4.costs == 0

    # Unit tests to story 4 + 2. from stories.md file

    # adding transfers from stories 2 and 4
    tArr6 = [transfer2, transfer4]
    rArr6 = [rec2, rec4]
    balance6 = calculate_balance(tArr6, rArr6)

    def test_balance_calc_for_example_story_06(self):
        # gross income is 500
        assert self.balance6.gross_income == 500
        # balance is 600 (with expenses = 60)
        assert self.balance6.balance == 440
        # vat balance: 0% from 500 - 20% from 60 -> vat = -10
        # you paid 10 EUR more vat than you should to treasury
        assert self.balance6.vat_due == -10
        # net balance: without vat equals gross income = 500-50
        assert self.balance6.net_balance == 450
        # income tax 19% from 450 (amount without vat) is 85.5.
        # have to pay to tax office
        assert self.balance6.flat_tax_due == 85.5
        # profit: 81% from net income (450) = 364.5
        # and can be transfer to personal bank account
        assert self.balance6.profit_due == 364.5
        # there was one expense for 60
        assert self.balance6.costs == 60
