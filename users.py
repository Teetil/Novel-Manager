from setup import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, abort, request
from os import urandom

def get_all_users() -> list:
    sql = "SELECT id, name, role FROM users ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_user(name : str, password : str, role=0) -> int:
    sql = "INSERT INTO users (name, password, role) VALUES (:name, :password, :role)"
    try:
        db.session.execute(sql, {"name" : name, "password" : generate_password_hash(password), "role" : role})
        db.session.commit()
    except:
        return False
    return login(name, password)

def login(name : str, password : str) -> bool:
    sql = "SELECT id, name, password, role FROM users WHERE name=:name"
    user = db.session.execute(sql, {"name" : name}).fetchone()
    if not user:
        return False
    if not check_password_hash(user[2], password):
        return False
    session["user_id"] = user[0]
    session["user_name"] = user[1]
    session["user_role"] = user[3]
    session["csrf_token"] = urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def get_user_info(user_id : int) -> list:
    sql = "SELECT id, name FROM users WHERE id=:user_id"
    return db.session.execute(sql, {"user_id" : user_id}).fetchone()

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def check_role(role):
    if session["user_role"] < role:
        abort(403)