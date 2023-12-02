CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role_id INTEGER REFERENCES roles
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread TEXT,
    created_at TIMESTAMP,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE
);



INSERT INTO topics (topic) VALUES ('general');
INSERT INTO topics (topic) VALUES ('politics');
INSERT INTO topics (topic) VALUES ('economy');
INSERT INTO roles (role) VALUES ('user');
INSERT INTO roles (role) VALUES ('admin');