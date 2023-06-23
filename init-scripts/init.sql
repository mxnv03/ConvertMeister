CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    token uuid NOT NULL,
    status INT NOT NULL
);

CREATE TABLE filenames (
    id SERIAL PRIMARY KEY,
    token uuid NOT NULL,
    name text NOT NULL,
    nickname text NOT NULL
);