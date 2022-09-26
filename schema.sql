CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE novels (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    synopsis TEXT,
    author_id INTEGER REFERENCES authors
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE novel_tags (
    novel_id INTEGER REFERENCES novels,
    tag_id INTEGER REFERENCES tags
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password INTEGER,
    role INTEGER
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    content TEXT,
    created_at TIMESTAMP,
    novel_id INTEGER REFERENCES novels,
    rating INTEGER
);



CREATE TABLE followers (
    user_id INTEGER REFERENCES users,
    novel_id INTEGER REFERENCES users
);



CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users,
    receiver_id INTEGER REFERENCES users,
    name TEXT
);