import sqlite3
import os

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "bill", "password")
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

users = [(2, "joe", "password"), (3, "tim", "password")]
cursor.executemany(insert_query, users)
selete_querey = "SELECT * FROM users"
for row in cursor.execute(selete_querey):
    print(row)

connection.commit()
connection.close()

# Clean up data.db file
# os.remove("data.db")
