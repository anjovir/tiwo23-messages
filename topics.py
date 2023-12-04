from db import db
import users
from sqlalchemy.sql import text


def add_topic(topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO topics (topic) VALUES (:topic)")
    db.session.execute(sql, {"topic":topic})
    db.session.commit()
    return True