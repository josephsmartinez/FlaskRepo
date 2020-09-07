from flask import request
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required, JWT

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        data = Item().search_items(name=name)
        return (data, 200) if data else (data, 404)

    def post(self, name):
        if Item().search_items(name=name):
            return {}, 400

        data = Item.parser.parse_args()

        item = {"name": name, "price": data.get("price")}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = [item for item in items if item.get("name") != name]
        return {}

    def put(self, name):
        # Request parsing
        data = Item.parser.parse_args()

        # data = request.get_json(silent=True)
        item = Item().search_items(name=name)
        new_item = {"name": name, "price": data.get("price")}
        if item:
            for item in items:
                if item.get("name") == name:
                    item.update(new_item)
            return {}, 200
        else:
            items.append(new_item)
            return {}, 201

    @staticmethod
    def search_items(name=None):
        return {
            k: v for item in items if item.get("name") == name for k, v in item.items()
        }

    def add_item_to_list(item: dict):
        name = item.get("name")
        price = item.get("price")
        if not (name or price):
            raise ItemKeyError("Cannot create item with missing name or price!")
        items.append({"name": item.get("name"), "price": item.get("price")})


class ItemList(Resource):
    def get(self):
        return items
