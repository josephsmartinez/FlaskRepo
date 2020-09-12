from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {}, 500

        return store.json(), 201

    def delete():
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {}, 200


class StoreList(Resource):
    def get(self, name):
        return [store.json() for store in StoreModel.query.all()]

