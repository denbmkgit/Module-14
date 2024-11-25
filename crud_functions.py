import sqlite3
from random import randint

connection = sqlite3.connect("products_data_d_3.db")
cursor = connection.cursor()


def initiata_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT ,
    price INT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email INT NOT NULL,
    age INT NOT NULL,
    balance NOT NULL
    );
    ''')


def add_user(username, email, age):
    initiata_db()
    if is_included(username) == False:
        cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                       (f'{username}', f'{email}', f'{age}', 1000))
        connection.commit()


def get_all_products():
    initiata_db()
    cursor.execute("SELECT * FROM Products")
    connection.commit()
    return cursor.fetchall()


def is_included(username):
    check_user_exists = cursor.execute("SELECT username FROM Users WHERE username = ?",
                                       (username,)).fetchone()
    if check_user_exists == None:
        return False
    elif check_user_exists[0] == username:
        return True
    connection.commit()


connection.commit()
# connection.close()


# for i in range(1,5):
#     cursor.execute("INSERT INTO Products(title, description, price) VALUES (?, ?, ?)",
#                    (f'Продукт{i}', f'Описание{i}', f'Цена {i*100}'))


# print(get_all_products()[1])


# cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)",
#                    ('Ivan', 'iv@gmail.com', '22', 1000))


# initiata_db()


# print(is_included('Ivan'))


# add_user('Ivan', 'iv@gmail.com', 22)


# cursor.execute("DELETE FROM Users WHERE username = ?", ('den',))
