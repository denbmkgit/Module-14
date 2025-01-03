import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute("DELETE FROM Users WHERE id = ?", ("6",))

# cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (500, "5" ))

# cursor.execute("SELECT * FROM Users")
# for user in cursor.fetchall():
#     print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

# cursor.execute("SELECT COUNT(*) FROM Users")
# all_users = cursor.fetchone()[0]

# cursor.execute("SELECT SUM(balance) FROM Users")
# sum_balance = cursor.fetchone()[0]

# print(sum_balance / all_users)

cursor.execute(("SELECT AVG(balance) FROM Users"))
avg_balance = cursor.fetchone()[0]
print(avg_balance)

connection.commit()
connection.close()
