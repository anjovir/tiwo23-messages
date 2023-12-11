from db import db
import users
from sqlalchemy.sql import text

def get_list(topic_id):
    sql = text("SELECT T.thread, U.username, T.created_at, T.topic_id, T.id FROM threads T, users U WHERE T.user_id=U.id AND T.topic_id=:topic_id ORDER BY T.id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_thread(thread_id):
    sql = text("SELECT T.thread, U.username, T.created_at, U.id FROM threads T, users U WHERE T.user_id=U.id AND T.id=:thread_id ORDER BY T.id")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()

def get_topic(topic_id):
    sql = text("SELECT T.topic, T.id, T.is_secret FROM topics T WHERE T.id=:topic_id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()

def edit_t(t_id, thread):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("UPDATE threads SET thread=:thread, created_at=NOW() WHERE id=:t_id")
    db.session.execute(sql, {"thread":thread, "t_id":t_id})
    db.session.commit()
    return True

def delete_t(t_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("DELETE FROM threads WHERE id=:t_id")
    db.session.execute(sql, {"t_id":t_id})
    db.session.commit()
    return True
