from pycountant.calculations import BalanceOfFinances
from pycountant.sample_data import TRANSFERS, RECEIPTS, RECEIPTS_ANY


def main():
    rec1, rec2, rec3 = RECEIPTS
    print()
    print(rec1)
    print()
    tr_arr = TRANSFERS
    balance = BalanceOfFinances(tr_arr)

    print(balance.tr_arr)

    print()
    print(
        "Calculations for: Incoming transfer based on invoices",
        rec1.amount,
        "with vat = 30% (with net amount, without indicated tax) and",
        rec2.amount,
        "with 0 vat and one outgoing transfer for",
        rec3.amount,
        "with vat = 30%:",
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
