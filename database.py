import sqlite3
from datetime import datetime

connection = sqlite3.connect('kfc.db')

sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, user_name TEXT, phone_number TEXT,'
            ' reg_date DATETIME);')

sql.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_price REAL, pr_quantity INTEGER, '
            'pr_desc TEXT, pr_photo TEXT, reg_date DATETIME);')

sql.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, pr_id INTEGER, pr_name TEXT, pr_count INTEGER, total_price REAL);')


connection.commit()

list_id = [i[0] for i in sql.execute('SELECT user_id FROM users').fetchall()]

def add_user(user_id, user_name, phone_number):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users (user_id, user_name, phone_number, reg_date) VALUES (?, ?, ?, ?);', (user_id, user_name, phone_number, datetime.now()))
    connection.commit()

def add_product(pr_name, pr_price, pr_quantity, pr_desc, pr_photo):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO products (pr_name, pr_price, pr_quantity, pr_desc, pr_photo, reg_date) VALUES '
                '(?, ?, ?, ?, ?, ?);', (pr_name, pr_price, pr_quantity, pr_desc, pr_photo, datetime.now()))

    connection.commit()

def pr_id_name():
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    data = sql.execute('SELECT pr_id, pr_name, pr_quantity FROM products;').fetchall()
    products_list = [[i[0], i[1]] for i in data if i[2] > 0]
    return products_list

def get_exact_product(pr_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    data = sql.execute('SELECT pr_name, pr_price, pr_desc, pr_photo FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    return data

def add_to_cart(user_id, pr_id, pr_name, pr_count, pr_price):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    total_price = pr_count * pr_price
    pr_id_list = [i[0] for i in sql.execute('SELECT pr_id FROM cart WHERE user_id=?;', (user_id,)).fetchall()]

    if pr_id not in pr_id_list:
        sql.execute('INSERT INTO cart (user_id, pr_id, pr_name, pr_count, total_price) VALUES (?, ?, ?, ?, ?);',
                    (user_id, pr_id, pr_name, pr_count, total_price))
        connection.commit()

    else:
        data = sql.execute('SELECT pr_count, total_price FROM cart WHERE pr_id=? AND user_id=?;',
                           (pr_id,user_id)).fetchone()
        print(data)

        sql.execute('UPDATE cart SET pr_count=? WHERE pr_id=? AND user_id=?;', (data[0] + pr_count, pr_id, user_id))
        sql.execute('UPDATE cart SET total_price=? WHERE pr_id=? AND user_id=?;', (data[1] + total_price, pr_id, user_id))
        connection.commit()

def get_exact_cart(user_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    cart = sql.execute('SELECT pr_name, pr_count, total_price, pr_id FROM cart WHERE user_id=?;', (user_id,)).fetchall()
    return cart

def get_cart_id_name(user_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    cart = sql.execute('SELECT pr_id, pr_name FROM cart WHERE user_id=?;', (user_id,)).fetchall()
    return cart


def delete_exact_cart(user_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    connection.commit()

def delete_exact_product_from_cart(user_id, pr_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM cart WHERE user_id=? AND pr_id=?;', (user_id,pr_id))
    connection.commit()

def order(pr_id, quantity):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    current = sql.execute('SELECT pr_quantity FROM products WHERE pr_id=?;', (pr_id,)).fetchone()[0]

    sql.execute('UPDATE products SET pr_quantity=? WHERE pr_id=?;', (current - quantity,pr_id))
    connection.commit()

def get_exact_product_quantity(pr_id):
    connection = sqlite3.connect('kfc.db')
    sql = connection.cursor()

    data = sql.execute('SELECT pr_quantity FROM products WHERE pr_id=?;', (pr_id,)).fetchone()[0]
    return data