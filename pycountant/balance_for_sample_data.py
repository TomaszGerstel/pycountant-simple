from pycountant.calculations import calculate_balance
from pycountant.sample_data import TRANSFERS_ANY, RECEIPTS_ANY
from pycountant.schemas import Transfer, Receipt


def calculate_balance_for_sample_data():
    tr_arr = []
    rec_arr = []

    for transfer in TRANSFERS_ANY:
        t = Transfer(
            id=transfer.get("id"),
            transfer_type=transfer.get("transfer_type"),
            amount=transfer.get("amount"),
            receipt_id=transfer.get("receipt_id"),
            from_=transfer.get("from_"),
            to_=transfer.get("to_"),
            descr=transfer.get("descr")
        )
        tr_arr.append(t)

    for receipt in RECEIPTS_ANY:
        r = Receipt(
            id=receipt.get("id"),
            amount=receipt.get("amount"),
            client=receipt.get("client"),
            worker=receipt.get("worker"),
            vet_value=receipt.get("vat_value"),
            net_amount=receipt.get("net_amount"),
            vat_percentage=receipt.get("vat_percentage"),
            descr=receipt.get("descr")
        )
        rec_arr.append(r)

    balance = calculate_balance(tr_arr, rec_arr)
    return balance
