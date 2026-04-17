payments = [
    {
        'payment_id': 'P001',
        'user_id': 'U123',
        'date': '2026-01-15',
        'items': [
            {'item_id': 'I1', 'amount': 100.50, 'category': 'electronics'},
            {'item_id': 'I2', 'amount': 50.25, 'category': 'books'}
        ]
    },
    {
        'payment_id': 'P002',
        'user_id': 'U123',
        'date': '2026-01-20',
        'items': [
            {'item_id': 'I3', 'amount': 200.00, 'category': 'electronics'}
        ]
    }
]
from collections import Counter
import pandas as pd
#   user_id  total_payments  total_amount  avg_amount_per_payment top_category
# 0    U123               2        350.75                  175.38  electronics
result = {}
def summarized_payments(payments):
    for payment in payments:
        payment_id = payment.get('payment_id')
        user_id = payment.get('user_id')
        if user_id not in result:
            result[user_id] = {'total_payments':0 ,'total_amount': 0, 'categories':[]} 
        result[user_id]['total_payments'] += 1
        items = payment.get('items')
        for item in items:
            amount = item.get('amount')
            category = item.get('category')
            result[user_id]['total_amount'] += amount
            result[user_id]['categories'].append(category)
    output = []
    for k,v in result.items():
        total_payments = v.get('total_payments')
        total_amount = v.get('total_amount')
        avg_amount = round(total_amount/total_payments,2)
        categories = v.get('categories')
        most_common_category = Counter(categories).most_common(1)[0][0]
        record = {
            'user_id' : k,
            'total_amount' : total_amount,
            'avg_amount':avg_amount,
            'category':most_common_category
        }
        output.append(record)
    df = pd.DataFrame(output)
    return df

if __name__ == '__main__':
    result = summarized_payments(payments)
    print(result)


