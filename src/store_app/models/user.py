import sqlite3
from flask import request
from flask_restful import Resource, reqparse
import lib.config as config


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect(config.USER_DB_PATH)
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
    def find_by_id(cls, _id: int):
        connection = sqlite3.connect(config.USER_DB_PATH)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        results = cursor.execute(query, (_id,))
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
        data = UserRegister.parser.parse_args()
        username = data.get("username")
        password = data.get("password")
        if User.find_by_username(username):
            return {}, 400

        connection = sqlite3.connect(config.USER_DB_PATH)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()

        return {}, 201
