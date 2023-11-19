from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT M.content, U.username, M.sent_at, M.thread_id FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_by_topic(topic_id):
    sql = text("SELECT M.content, U.username, M.sent_at, M.topic_id FROM messages M, users U WHERE M.user_id=U.id AND M.topic_id=:topic_id  ORDER BY M.id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()


def send(content):
    user_id = users.user_id()
    thread_id = 1
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, user_id, sent_at, thread_id) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def newt(thread, message):
    topic_id= 1
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO threads (thread, user_id, topic_id) VALUES (:thread, :user_id, :topic_id) RETURNING id")
    result = db.session.execute(sql, {"thread":thread, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    thread_id = result.fetchone()[0]
    sql = text("INSERT INTO messages (content, user_id, sent_at, thread_id, topic_id) VALUES (:content, :user_id, NOW(),:thread_id, :topic_id)")
    db.session.execute(sql, {"content":message, "user_id":user_id, "thread_id":thread_id, "topic_id":topic_id})
    db.session.commit()
    return True