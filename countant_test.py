import unittest
import exceptions
from calculations import BalanceOfFinances
from model import DefaultVatInvoice, TransferType, Transfer, NoVatInvoice


class CountantTests(unittest.TestCase):
    invoice1 = DefaultVatInvoice(
        amount=100,
        client="me",
        worker="worker_from_some_firm",
        descr="for_some_shopping",
    )
    invoice2 = DefaultVatInvoice(
        amount=500.00,
        client="client2_on_Invoice",
        worker="worker_on_invoice",
        descr="descr",
    )
    invoice3 = NoVatInvoice(
        amount=352.5, client="client1", worker="me", descr="example_descr"
    )

    # out transfer without optional values
    transfer1 = Transfer(
        invoice=invoice1, amount=100, transfer_type=TransferType.OUT_TRANSFER
    )
    # transfer without amout, taking amout from invoice
    transfer2 = Transfer(
        invoice=invoice2,
        _from="client2",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    # transfer with no vat type invoice
    transfer3 = Transfer(
        invoice=invoice3,
        amount=352.50,
        _from="client1",
        _to="me",
        descr="example_desc",
        transfer_type=TransferType.IN_TRANSFER,
    )
    # transfer with negative value
    transfer4 = Transfer(amount=-650, transfer_type=TransferType.OUT_TRANSFER)
    # list of transfers
    transfers_list = [transfer1, transfer2, transfer3]
    # list with wrong transfer4
    transfers_list2 = [transfer1, transfer3, transfer4]

    balance = BalanceOfFinances(transfers_list)

    def test_methods_from_balance_finances_should_return_known_gross_balance(self):
        """500+352.5(in transfers)-100(out transfer)=752.5"""
        result = self.balance.balance
        self.assertEqual(752.5, result)

    # to add: get costs, gross income,

    def test_methods_from_amount_balance_should_return_known_net_balance(
        self,
    ):  # poprawić
        """500 in with 30% vat + 352.5 without vat - 100 with 30% out transfer = 385 (round) + 352.5 - 77
        = 660 (round)"""
        """385(round with default vat value 30%)+271(in transfers)-100(out transfer)=556 (round)"""
        result = self.balance.net_balance
        self.assertEqual(660, result.__round__())

    def test_methods_from_amount_balance_should_return_known_vat_balance(self):
        """30% vat from 500 in transfer - 30% vat from 100 out transfer = 92 (round),
        (plus one transfer includes no vat invoice)"""
        result = self.balance.vat_balance
        self.assertEqual(92, result.__round__())

        # to add: income tax, profit

    # single object test of methods, not null tests?
    # test stories
    # exception tests, negative value
