import sqlite3

connection =sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY, 
username TEXT NOT NULL, 
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL 
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS ind_email ON Users (email)")

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, balance, age) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", "1000", f"{i}0"))

for i in range(1, 11):
    if i % 2 == 0:
        cursor.execute("UPDATE Users SET balance = ? WHERE age = ?", (500, f"{i}0" ))

for i in range(1, 11):
    if (i - 1) % 3 == 0:
        cursor.execute("DELETE FROM Users WHERE age = ?", (f"{i}0",))

cursor.execute("SELECT * FROM Users WHERE age != ?", ("60",))
for user in cursor.fetchall():
    print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

connection.commit()
connection.close()