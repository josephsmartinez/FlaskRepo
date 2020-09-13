import os
from colorama import init
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# Application configs
import lib.config as config

# JWT Handlers
from lib.security import auth, indentity, security_error_handler

# DataBase Helpers
from lib.database import DataBase

# Resources for routes
from resources.items import Item, ItemList
from resources.user import User, UserRegister
from resources.store import Store, StoreList

# Applications should initialise Colorama
init(autoreset=True)

# Configure application
app = Flask(__name__)
api = Api(app)
app.secret_key = config.APP_KEY

# Configure JWT
jwt = JWT(app, auth, indentity)
jwt.jwt_error_handler(security_error_handler)
app.config["PROPAGATE_EXCEPTIONS"] = True

# If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# SQLALCHEMY_BINDS = {"users": "sqlite:///var/users.db", "items": "sqlite:///var/items.db"}
# app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS


@app.before_first_request
def create_table():
    """
    Create all tables before the appplication starts.
    """
    DataBase.alchemy.init_app(app)
    DataBase.alchemy.create_all()


# Configure resources/routes
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")


# Init application
if __name__ == "__main__":
    app.run(port=5000, debug=True)
