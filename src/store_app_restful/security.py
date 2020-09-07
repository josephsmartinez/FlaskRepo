# -*- coding: utf-8 -*-
"""
    flask_jwt - This file contains methods used by the JWT class.
    ~~~~~~~~~

    Flask-JWT module 
    https://pythonhosted.org/Flask-JWT/_modules/flask_jwt.html#JWT.jwt_error_handler
"""
from werkzeug.security import safe_str_cmp
from user import User
from flask_jwt import JWTError


def auth(username, password):
    user = User.find_by_username(username)
    # TODO: Handle None user return
    if user is None:
        raise JWTError(Exception, "User not found", status_code=404)
    return user if safe_str_cmp(user.password, password) else None


def indentity(payload):
    user = User.find_by_username(payload.get("identity"))
    return user if user.id == user_id else None


def security_error_handler(e):
    return "{}".format(e.description), e.status_code

