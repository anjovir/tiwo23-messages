from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password,role_id) VALUES (:username,:password,1)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def change_password(user_id, old_password, new_password):
    sql = text("SELECT id, password FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    user = result.fetchone()
    if check_password_hash(user.password, old_password):
        hash_value = generate_password_hash(new_password)
        try:
            sql = text("UPDATE users SET password=:new_password WHERE id=:user_id")
            db.session.execute(sql, {"new_password":hash_value, "user_id":user_id})
            db.session.commit()
        except:
            return False
    return True

def create_admin():
    admin_username = "admin"
    admin_password = getenv("ADMIN_PASSWORD")

    sql = text("SELECT id FROM users WHERE role_id='2'")
    result = db.session.execute(sql)
    id = result.fetchone()

    if id is None:
        hash_value = generate_password_hash(admin_password)
        sql = text("INSERT INTO users (username,password,role_id) VALUES (:username,:password,'2')")
        db.session.execute(sql, {"username":admin_username, "password":hash_value})
        db.session.commit()


