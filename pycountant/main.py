from pycountant.calculations import BalanceOfFinances
from pycountant.sample_data import TRANSFERS, INVOICES, INVOICES_ANY


def main():
    print(INVOICES_ANY)

    inv1, inv2, inv3 = INVOICES
    print(inv1)
    tr_arr = TRANSFERS
    balance = BalanceOfFinances(tr_arr)

    print(balance.tr_arr)

    print()
    print(
        "Calculations for: Incoming transfer based on invoices",
        inv1.amount,
        "with default vat = 30% and",
        inv2.amount,
        "with 0 vat and one outgoing transfer for",
        inv3.amount,
        "with default vat = 30%:",
    )

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
