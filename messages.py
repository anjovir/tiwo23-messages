from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT M.content, U.username, M.sent_at, M.thread_id FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_by_topic(topic_id):
    sql = text("""SELECT M.content, U.username, M.sent_at, M.topic_id
               FROM messages M, users U 
               WHERE M.user_id=U.id AND M.topic_id=:topic_id 
               ORDER BY M.id""")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_topics_list():
    sql = text("SELECT * FROM topics")
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_by_thread(thread_id):
    sql = text("""SELECT M.content, U.username, M.sent_at, M.thread_id, M.topic_id, M.user_id, M.id
               FROM messages M, users U 
               WHERE M.user_id=U.id AND M.thread_id=:thread_id 
               ORDER BY M.id""")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def count_messages(thread_id):
    sql = text("SELECT COUNT(*) FROM threads WHERE id=:thread_id")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()

def send(content, thread_id, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, user_id, sent_at, thread_id, topic_id) VALUES (:content, :user_id, NOW(), :thread_id, :topic_id)")
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id, "topic_id":topic_id})
    db.session.commit()
    return True

def newt(thread, message,topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO threads (thread, user_id, topic_id, created_at) VALUES (:thread, :user_id, :topic_id, NOW()) RETURNING id")
    result = db.session.execute(sql, {"thread":thread, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    thread_id = result.fetchone()[0]
    sql = text("INSERT INTO messages (content, user_id, sent_at, thread_id, topic_id) VALUES (:content, :user_id, NOW(),:thread_id, :topic_id)")
    db.session.execute(sql, {"content":message, "user_id":user_id, "thread_id":thread_id, "topic_id":topic_id})
    db.session.commit()
    return True

def get_message(m_id):
    sql = text("SELECT M.content, M.id FROM messages M WHERE  M.id=:m_id")
    result = db.session.execute(sql, {"m_id":m_id})
    return result.fetchone()

def edit_m(m_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("UPDATE messages SET content=:content, sent_at=NOW() WHERE id=:m_id")
    db.session.execute(sql, {"content":content, "m_id":m_id})
    db.session.commit()
    return True

def delete_m(m_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("DELETE FROM messages WHERE id=:m_id")
    db.session.execute(sql, {"m_id":m_id})
    db.session.commit()
    return True
    
def search(query):
    sql = text("""SELECT M.content, U.username, M.sent_at, T.thread, T.id 
               FROM messages M, users U, threads T
               WHERE LOWER(M.content) LIKE LOWER(:query) AND M.user_id=U.id AND M.thread_id=T.id""")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()