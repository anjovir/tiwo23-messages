from db import db
import users
from sqlalchemy.sql import text

def get_list(topic_id):
    sql = text("SELECT T.thread, U.username, T.created_at, T.topic_id, T.id FROM threads T, users U WHERE T.user_id=U.id AND T.topic_id=:topic_id ORDER BY T.id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()