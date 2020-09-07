import sqlite3
from flask import request
from flask_restful import Resource, reqparse
import lib.config as config


class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        results = cursor.execute(query, (username,))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect(config.DBNAME)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        results = cursor.execut(query, (_id,))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        # TODO: Should only create one user and no dedups
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect(config.DBNAME)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data.get("username"), data.get("password")))
        connection.commit()
        connection.close()

        return {}, 201
