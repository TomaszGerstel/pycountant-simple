from pycountant.balance_for_sample_data import calculate_balance_for_sample_data
from pycountant.calculations import calculate_balance
from pycountant.sample_data import TRANSFERS, RECEIPTS, RECEIPTS_ANY, TRANSFERS_ANY


def main():
    rec1, rec2, rec3 = RECEIPTS
    print()
    print(rec1)
    print()
    tr_arr = TRANSFERS
    rec_arr = RECEIPTS
    balance = calculate_balance(tr_arr, rec_arr)

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
    print()
    print(balance.__repr__())
    balance2 = calculate_balance_for_sample_data()
    print(balance2.__repr__())


if __name__ == "__main__":
    main()
