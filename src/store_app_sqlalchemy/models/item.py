import sqlite3
import lib.config as config
from lib.database import DataBase as db


class ItemModel(db.alchemy.Model):

    # sqlalchemy settings
    __tablename__ = "items"
    # __bind_key__ = "items"

    id = db.alchemy.Column(db.alchemy.Integer, primary_key=True)
    name = db.alchemy.Column(db.alchemy.String(80))
    price = db.alchemy.Column(db.alchemy.Float(precision=2))

    store_id = db.alchemy.Column(db.alchemy.Integer, db.alchemy.ForeignKey("stores.id"))
    store = db.alchemy.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: str):
        self.name = name
        self.price = price
        self.store_id = store_id

    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(
            name=name
        ).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.alchemy.session.add(self)  # Does both UPDATE and INSERT
        db.alchemy.session.commit()

    def delete_from_db(self):
        db.alchemy.session.delete(self)
        db.alchemy.session.commit()

    def json(self):
        return {"name": self.name, "price": self.price}
