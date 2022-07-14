

import Calculations
from Model import DefaultVatInvoice, NoVatInvoice, Transfer, TransferType


def main():

    inv1 = DefaultVatInvoice(amount=1500.00, client="Burger King", worker="me", descr="data analysis")
    inv2 = NoVatInvoice(amount=2200, client="Biedronka", worker="me", descr="app")
    inv3 = DefaultVatInvoice(amount=300, client="me", worker="Allegro", descr="for hard_drive")

    t1 = Transfer(TransferType.IN_TRANSFER, invoice=inv1, amount=1500.00,
                  _from="Burger Queen", _to="me", descr="data analysis")
    print(t1)
    t2 = Transfer(TransferType.IN_TRANSFER, invoice=inv2, amount=2200.00, _from="Burger King",
                  _to="me", descr="gift")
    t3 = Transfer(TransferType.OUT_TRANSFER, invoice=inv3, _to="Allegro", _from="me", amount=300)
    tr_arr = [t1, t2, t3]
    balance = Calculations.BalanceOfFinances(tr_arr)

    print(balance.tr_arr)

    print()
    print("Calculations for: Incoming transfer based on invoices", inv1.amount, "with default vat = 30% and",
          inv2.amount, "with 0 vat and one outgoing transfer for", inv3.amount, "with default vat = 30%:")

    print()
    print("state of finances (balance), should equals income - costs:")
    print(balance.balance)
    print()
    print("income:")
    print(balance.gross_income)
    print()
    print("costs (outgoing):")
    print(balance.costs)
    print()
    print("net profit (less costs and VAT):")
    print(balance.net_balance)
    print()
    print("vat (to the treasury):")
    print(balance.vat_balance)
    print()
    print("income tax to the tax office (30%):")
    print(balance.income_tax_30)
    print()
    print("profit after tax:")
    print(balance.profit)


if __name__ == "__main__":
    main()
