

from database.models import Transaction, Product
from database.db import get_all


def get_all_transaction_out_by_product_id(product_id:int) -> list:

    all_transaction = Transaction.convert_to_Transactions(get_all(Transaction.get_all_transactions_query()))

    all_transaction_out = []
    for transaction in all_transaction:
        if transaction.transaction_type == "OUT":
            all_transaction_out.append(transaction)
            
    final_list = []
    for t in all_transaction_out:
        if t.product_id == product_id:
            final_list.append(t)
            
    return final_list

ts = get_all_transaction_out_by_product_id(5)
     
def average_days_for_number_of_purchases(transactions:list) -> int:
    for t in transactions:
        print(t.transaction_date)


average_days_for_number_of_purchases(ts)