def transform_data(data):
    result = []
    seen = set()
    for record in data:
        customer_id = record['customer_id']
        customer_name = record['customer_name']
        orders = record.get('orders',[])
        for order in orders:
            order_id = order['order_id']
            order_date = order['order_date']
            amount = order['amount']
            status = order['status']
            if status!= 'completed':
                continue
            if amount is None:
                continue
            if order_id in seen:
                continue
            seen.add(order_id)
            
            new_record = {
                'customer_id':customer_id, 
                'customer_name':customer_name, 
                'order_id':order_id, 
                'order_date':order_date,
                'amount':float(amount),
                'status':status
            }
            result.append(new_record)
    
    return result

                            