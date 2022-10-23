CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE novels (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    synopsis TEXT,
    author_id INTEGER REFERENCES authors,
    chapter_cnt INTEGER
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE novel_tags (
    novel_id INTEGER REFERENCES novels ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users ON DELETE CASCADE,
    content TEXT,
    created_at TIMESTAMP,
    novel_id INTEGER REFERENCES novels ON DELETE CASCADE,
    rating INTEGER
);



CREATE TABLE followers (
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    novel_id INTEGER REFERENCES novels ON DELETE CASCADE,
    last_update_cnt INTEGER
);
