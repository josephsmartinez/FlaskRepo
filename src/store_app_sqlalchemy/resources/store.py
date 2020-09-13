from flask_restful import Resource
from models.store import StoreModel
from http import HTTPStatus


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {}, HTTPStatus.NOT_FOUND

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {}, HTTPStatus.BAD_REQUEST
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {}, HTTPStatus.INTERNAL_SERVER_ERROR
        return store.json(), HTTPStatus.CREATED

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {}, HTTPStatus.OK
        return {}, HTTPStatus.NOT_FOUND


class StoreList(Resource):
    def get(self):
        return [store.json() for store in StoreModel.query.all()]

