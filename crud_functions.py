import sqlite3

connection =sqlite3.connect("initiate_db.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
discription TEXT,
price INTEGER NOT NULL
)
''')

def get_all_products():
    for user in cursor.execute("SELECT * FROM Users"):
        print(user)

# for i in range(1, 5):
#     cursor.execute("INSERT INTO Users (title, discription, price) VALUES (?, ?, ?)",
#                    (f"product{i}", f"product {i} is very good", f"{i}00", ))

# cursor.execute("INSERT INTO Users(title, discription, price) VALUES (?, ?, ?)",
#                ('product4', 'product 4 is very good', 400,))

# cursor.execute("UPDATE Users SET discription = ? WHERE id =?", ('product 3 is very good', '3'))

get_all_products()

connection.commit()
connection.close()
