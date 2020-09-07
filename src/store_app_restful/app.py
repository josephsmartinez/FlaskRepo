from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# Application configs
import lib.config as config

# JWT Handlers
from security import auth, indentity, security_error_handler

# DataBase Helpers
from database import DataBase

# Resources for routes
from items import Item, ItemList
from user import UserRegister

# Configure application
app = Flask(__name__)
api = Api(app)
app.secret_key = config.APP_KEY

# Configure JWT
jwt = JWT(app, auth, indentity)
jwt.jwt_error_handler(security_error_handler)

# Configure DataBase
db = DataBase(config.DBNAME)

# Configure resources/routes
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

# Init application
app.run(port=5000, debug=True)
