import os
import sqlite3


class DataBase:
    def __init__(self, name):
        self.name = name
        DataBase.create_empty_table(name)

    @staticmethod
    def create_empty_table(name):
        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
        cursor.execute(create_table)
        connection.commit()
        connection.close()

    @staticmethod
    def createdb_with_dummy_items(name):

        if os.path.isfile(name):
            print("Clearing create database and creating new.")
            os.remove(name)

        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        create_table = "CREATE TABLE users (id int, username text, password text)"
        cursor.execute(create_table)
        print("Created table: {}".format(name))

        users = [(1, "bill", "password"), (2, "joe", "password"), (3, "tim", "password")]
        insert_query = "INSERT INTO users VALUES (?,?,?)"
        cursor.executemany(insert_query, users)
        connection.commit()
        connection.close()
