from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv
import secrets

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["csrf_token"]

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

def check_csfr(csfr_token):
    if session["csrf_token"] != csfr_token:
        abort(403)

def check_membership(topic_id, user_id):
    sql = text("SELECT user_id, topic_id FROM secret_room WHERE user_id=:user_id AND topic_id=:topic_id")
    result = db.session.execute(sql, {"user_id":user_id, "topic_id":topic_id})

    if result.fetchone() is None:
        abort(403)

    

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
    admin_username = 'admin'
    admin_password = getenv("ADMIN_PASSWORD")

    sql = text("SELECT id FROM users WHERE role_id='2'")
    result = db.session.execute(sql)
    id = result.fetchone()

    if id is None:
        hash_value = generate_password_hash(admin_password)
        sql = text("INSERT INTO users (username,password,role_id) VALUES (:username,:password,'2')")
        db.session.execute(sql, {"username":admin_username, "password":hash_value})
        db.session.commit()

def check_if_admin(user_id):
    print(user_id)
    if user_id == 0 or user_id == None:
        return False
    sql = text("""  SELECT R.role
                    FROM users U
                    LEFT JOIN roles R ON U.role_id = R.id
                    WHERE U.id=:user_id;
                    """)

    result = db.session.execute(sql, {"user_id":user_id})
    result = result.fetchone()[0]
    if result == "admin":
        return True
    return False

def list_sroom_users(topic_id):
    sql = text("SELECT U.username, U.id, S.topic_id FROM secret_room S, Users U WHERE S.user_id=U.id AND topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def list_all_sroom_users():
    sql = text("SELECT U.username, U.id, S.topic_id FROM secret_room S, Users U WHERE S.user_id=U.id")
    result = db.session.execute(sql)
    return result.fetchall()

def list_users():
    sql = text("SELECT id, username FROM users")
    result = db.session.execute(sql)
    return result.fetchall()

def max_id():
    sql = text("SELECT MAX(id) FROM users")
    result = db.session.execute(sql)
    return result.fetchone()

def add_user(topic_id, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO secret_room (topic_id, user_id) VALUES (:topic_id, :user_id)")
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def remove_user(topic_id, user_id):
    if user_id == 0:
        return False
    sql = text("DELETE FROM secret_room WHERE topic_id=:topic_id AND user_id=:user_id")
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True