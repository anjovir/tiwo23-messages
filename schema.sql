CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    thread_id INTEGER REFERENCES threads,
    topic_id INTEGER REFERENCES topics
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread TEXT,
    created_at TIMESTAMP,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users
);