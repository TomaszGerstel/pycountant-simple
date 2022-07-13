import unittest

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