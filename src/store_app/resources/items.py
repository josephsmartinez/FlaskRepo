import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import lib.config as config
from models.item import ItemModel


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
        item = ItemModel(name, data.get("price"))

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        if ItemModel.find_by_name(name):
            ItemModel.delete(name)
            return {}, 200
        return {}, 404

    def put(self, name):
        # Request parsing
        data = Item.parser.parse_args()

        # data = request.get_json(silent=True)

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data.get("price"))

        if item:
            try:
                updated_item.update()
            except:
                return {}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {}, 500
        return updated_item.json(), 201


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(config.ITEM_DB_PATH)
        cursor = connection.cursor()
        query = "SELECT * FROM {}".format(config.ITEM_DB_NAME)
        rows = cursor.execute(query)
        items = [{"name": item[0], "price": item[1]} for item in rows.fetchall() if len(item) == 2]
        connection.close()
        return items
