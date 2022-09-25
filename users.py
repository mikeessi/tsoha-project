import os
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash

def login(name, password):
    sql = "SELECT password, id, user_role FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["username"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def check_username(name):
    sql = "SELECT name FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":name})
    user = result.fetchone()
    if not user:
        return True
    return False

def create_account(name, password, user_role):
    password_hash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, user_role)
                 VALUES (:name, :password, :user_role)"""
        db.session.execute(sql, {"name":name, "password":password_hash, "user_role":user_role})
        db.session.commit()
    except:
        return False
    return login(name, password)

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def check_csrf_token(token):
    if session["csrf_token"] != token:
        abort(403)

def check_user_access(role):
    if session.get("user_role", 0) < role:
         abort(403)
