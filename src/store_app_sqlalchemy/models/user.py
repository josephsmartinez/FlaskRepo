import sqlite3
from flask import request
from flask_restful import Resource, reqparse
import lib.config as config
from lib.database import DataBase as db


class UserModel(db.alchemy.Model):

    # sqlalchemy settings
    __tablename__ = "users"
    # __bind_key__ = "users"

    id = db.alchemy.Column(db.alchemy.Integer, primary_key=True)
    username = db.alchemy.Column(db.alchemy.String(80))
    password = db.alchemy.Column(db.alchemy.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.alchemy.session.add(self)
        db.alchemy.session.commit()

    def delete_from_db(self):
        db.alchemy.session.delete(self)
        db.alchemy.session.commit()

    def json(self):
        # Find the user id.
        return {"id": self.id, "username": self.username}

