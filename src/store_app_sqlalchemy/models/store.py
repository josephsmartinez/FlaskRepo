from lib.database import DataBase as db


class StoreModel(db.alchemy.Model):

    # sqlalchemy settings
    __tablename__ = "stores"
    # __bind_key__ = "stores"

    id = db.alchemy.Column(db.alchemy.Integer, primary_key=True)
    name = db.alchemy.Column(db.alchemy.String(80))

    item = db.alchemy.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str, price: float):
        self.name = name

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
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}
