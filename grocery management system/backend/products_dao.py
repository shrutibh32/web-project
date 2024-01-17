from sql_connection import get_sql_connection
def get_all_products(connection):
    cursor = connection.cursor()
    
    query = ("SELECT products.product_id,products.name,products.uomid,products.priceperunit,uom.uomname FROM grocerystore.products INNER JOIN grocerystore.uom on grocerystore.products.uomid=grocerystore.uom.uomid")
    cursor.execute(query)
    response = []
    for (product_id, name, uomid, priceperunit,uomname) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uomid,
            'price_per_unit': priceperunit,
            'uom_name': uomname
        })
    return response
def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("insert into grocerystore.products"
             "(name,uomid,priceperunit)"
             "values(%s,%s,%s)")
    data = (product['name'], product['uomid'], product['priceperunit'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid
def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid
if __name__ == '__main__':
   connection = get_sql_connection()
   print(delete_product(connection,3))


    