from flask import Flask, jsonify, request

app = Flask(__name__)


stores = [
    {
        "name": "My Wonderful Store",
        "items": [{"item": "Boot", "price": 15.99}, {"item": "Hat", "price": 10.99}],
    },
    {
        "name": "Some other store",
        "items": [{"item": "TV", "price": 99.99}, {"item": "Chair", "price": 20.99}],
    },
    {
        "name": "Pizza Shop",
        "items": [{"item": "pizza", "price": 3.99}, {"item": "soda", "price": 1.99}],
    },
]


@app.route("/store")
def get_stores():
    """
    GET /store
    """
    return jsonify({"stores": stores})


@app.route("/store", methods=["POST"])
def create_store():
    """
    POST /store data: {name:}
    """
    data = request.get_json()
    new_store = {"name": data.get("name"), "item": data.get("items")}
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def get_store(name):
    """
    GET /store/<string:name>
    """
    data = {
        k: v for store in stores if store.get("name") == name for k, v in store.items()
    }
    return jsonify(data)


@app.route("/store/<string:name>/name", methods=["POST"])
def create_store_by_name(name):
    """
    POST /store/<string:name>/item {name:, price:}
    """
    data = {"name": name, "items": []}
    stores.append(data)
    return jsonify(data)


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    """
    POST /store/<string:name>/item
    """
    data = request.get_json()
    for store in stores:
        if store.get("name") == name:
            store.get("items").append(
                {"name": data.get("name"), "price": data.get("price")}
            )
    return jsonify(data)


@app.route("/store/<string:store_name>/item/<string:search_item>")
def get_item_in_store(store_name, search_item):
    """
    GET /store/<string:name>/item
    """
    data = {
        k: v
        for store in stores
        if store.get("name") == store_name
        for item in store.get("items")
        if item.get("item") == search_item
        for k, v in item.items()
    }
    return jsonify(data)


@app.route("/store/items")
def get_items_from_stores():
    """
    GET /store/items
    """
    data = [item for store in stores for item in store.get("items")]
    return jsonify(data)


app.run(port=5000)
