import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import lib.config as config
from models.item import ItemModel
from http import HTTPStatus


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred save_to_dbing the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {}, 200
        return {}, 404

    def put(self, name):
        # Request parsing
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data.get("price")
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return [item.json() for item in ItemModel.query.all()]
