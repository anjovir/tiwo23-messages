from db import db
import users
from sqlalchemy.sql import text


def add_topic(topic, is_secret):       
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (topic, is_secret) VALUES (:topic, :is_secret) RETURNING id")
    result = db.session.execute(sql, {"topic":topic, "is_secret":is_secret})
    topic_id = result.fetchone()[0]
    if create_secret_room(topic_id):
        db.session.commit()
        return True
    return False

def delete_topic(topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("DELETE FROM topics WHERE id=:topic_id")
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()
    return True

def create_secret_room(topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO secret_room (topic_id, user_id) VALUES (:topic_id, :user_id)")
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def is_secret(topic_id):
    sql = text("SELECT is_secret FROM topics WHERE id=:topic_id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()[0]
