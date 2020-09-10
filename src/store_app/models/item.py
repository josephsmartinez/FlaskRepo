import sqlite3
import lib.config as config


class ItemModel:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(config.ITEM_DB_PATH)
        cursor = connection.cursor()

        query = "SELECT * FROM {} WHERE name=?".format(config.ITEM_DB_NAME)
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()

        if row:
            return cls(*row)
        return None

    def update(self):
        connection = sqlite3.connect(config.ITEM_DB_PATH)
        cursor = connection.cursor()

        query = "UPDATE {} SET price=? WHERE name=?".format(config.ITEM_DB_NAME)
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def insert(self):
        connection = sqlite3.connect(config.ITEM_DB_PATH)
        cursor = connection.cursor()
        query = "INSERT INTO {} VALUES (?, ?)".format(config.ITEM_DB_NAME)
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    @staticmethod
    def delete(name):
        connection = sqlite3.connect(config.ITEM_DB_PATH)
        cursor = connection.cursor()
        query = "DELETE FROM {} WHERE name=?".format(config.ITEM_DB_NAME)
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    @staticmethod
    def search_items(name=None):
        return {k: v for item in items if item.get("name") == name for k, v in item.items()}

    def add_item_to_list(item: dict):
        name = item.get("name")
        price = item.get("price")
        if not (name or price):
            raise ItemKeyError("Cannot create item with missing name or price!")
        items.append({"name": item.get("name"), "price": item.get("price")})

    def json(self):
        return {"name": self.name, "price": self.price}
