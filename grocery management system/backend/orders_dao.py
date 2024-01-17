from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("insert into grocerystore.orders"
                   "(customer_name,total,datetime)"
                   "values(%s,%s,%s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    orderid = cursor.lastrowid

    order_details_query = ("insert into grocerystore.order_details "
                           "(orderid, productid, quantity, totalprice)"
                           "values (%s, %s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            orderid,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['totalprice'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return orderid

def get_order_details(connection, orderid):
    cursor = connection.cursor()

    query = "SELECT * from order_details where orderid = %s"

    query = "SELECT order_details.orderid, order_details.quantity, order_details.totalprice, "\
            "products.name, products.priceperunit FROM grocerystore.order_details LEFT JOIN grocerystore.products on " \
            "grocerystore.order_details.productid = grocerystore.products.product_id where grocerystore.order_details.orderid = %s"

    data = (orderid, )

    cursor.execute(query, data)

    records = []
    for (orderid, quantity, totalprice, name, priceperunit) in cursor:
        records.append({
            'order_id': orderid,
            'quantity': quantity,
            'total_price': totalprice,
            'product_name': name,
            'price_per_unit': priceperunit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (orderid, customer_name, total, datetime) in cursor:
        response.append({
            'orderid': orderid,
            'customer_name': customer_name,
            'total': total,
            'datetime': datetime,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['orderid'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '500',
    #     'datetime': datetime.now(),
    #     'order_details': [
    #         {
    #             'product_id': 1,
    #             'quantity': 2,
    #             'total_price': 50
    #         },
    #         {
    #             'product_id': 3,
    #             'quantity': 1,
    #             'total_price': 30
    #         }
    #     ]
    # }))