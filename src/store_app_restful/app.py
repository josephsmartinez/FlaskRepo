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
from lib.items import Item, ItemList
from lib.user import UserRegister

# Applications should initialise Colorama
init(autoreset=True)

# Configure application
app = Flask(__name__)
api = Api(app)
app.secret_key = config.APP_KEY

# Configure JWT
jwt = JWT(app, auth, indentity)
jwt.jwt_error_handler(security_error_handler)

# Configure DataBase
DataBase.create_user_table(config.USER_DB_PATH, new=True)
DataBase.create_item_table(config.ITEM_DB_PATH, new=True)

# Configure resources/routes
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

# Init application
if __name__ == '__main__':
    app.run(port=5000, debug=True)
