import unittest
import exceptions
from main import Transfer, sum_transfers, sum_transfers_generator, TransferType, AmountBalance, \
    DefaultVatInvoice, NoVatInvoice


class CountantTests(unittest.TestCase):

    invoice1 = DefaultVatInvoice(amount=500.00, client="client2_on_Invoice", worker="worker_on_invoice", descr="descr")
    invoice2 = DefaultVatInvoice(amount=352.5, client="client1", worker="me", descr="example_descr")
    # invoice3 = NoVatInvoice()
    # transfer without optional values
    transfer1 = Transfer(amount=100, transfer_type=TransferType.OUT_TRANSFER)
    # transfer without amout, taking amout from invoice
    transfer2 = Transfer(invoice=invoice1, _from="client2", _to="me", descr="example_desc",
                         transfer_type=TransferType.IN_TRANSFER)
    transfer3 = Transfer(invoice=invoice2, amount=352.50, _from="client1", _to="me", descr="example_desc",
                         transfer_type=TransferType.IN_TRANSFER)
    # transfer with negative value
    transfer4 = Transfer(amount=-650, transfer_type=TransferType.OUT_TRANSFER)
    transfers_list = [transfer1, transfer2, transfer3]
    transfers_list2 = [transfer1, transfer3, transfer4]

    balance = AmountBalance(transfers_list)

    def test_sum_transfers_for_known_amounts(self):
        """sum_transfer should give sum of amounts from Transfer objects == 952.5,
        (for example amounts 100, 500, 350)"""
        result = sum_transfers(self.transfers_list)
        self.assertEqual(952.5, result)

    def test_sum_transfers_generator_for_known_amounts(self):
        """sum_transfer_generator should give sum of amounts from Transfer objects == 952.5,
        (for example amounts 100, 500, 350)"""
        result = sum_transfers_generator(self.transfers_list)
        self.assertEqual(952.5, result)

    def test_sum_transfer_should_raise_value_error(self):
        """method should raise exception for negative value"""
        self.assertRaises(exceptions.NegativeValueError, sum_transfers, self.transfers_list2)

    def test_methods_from_amount_balance_should_return_known_gross_balance(self):
        """500+352.5(in transfers)-100(out transfer)=752.5"""
        result = self.balance.balance
        self.assertEqual(752.5, result)

    def test_methods_from_amount_balance_should_return_known_net_balance(self):
        """385(round withdefault vat value 30%)+271(in transfers)-100(out transfer)=556 (round)"""
        result = self.balance.net_balance
        self.assertEqual(556, result.__round__())

    def test_methods_from_amount_balance_should_return_known_vat_balance(self):
        """752.5 - 556 = 197 (round)"""
        result = self.balance.vat_balance
        self.assertEqual(197, result.__round__())
