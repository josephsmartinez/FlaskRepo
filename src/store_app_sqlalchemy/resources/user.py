import sqlite3
from flask import request
from flask_restful import Resource, reqparse
import lib.config as config
from models.user import UserModel


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
        if UserModel.find_by_username(username):
            return {}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {}, 201
