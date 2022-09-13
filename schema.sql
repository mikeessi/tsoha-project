CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    user_role INTEGER
);

CREATE TABLE gyms (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT
);

CREATE TABLE  boulders (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES gyms,
    difficulty INTEGER,
    routesetter_id INTEGER REFERENCES users
);

CREATE TABLE topped_boulders (
    id SERIAL PRIMARY KEY,
    boulder_id INTEGER REFERENCES boulders
    user_id INTEGER REFERENCES users
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    boulder_id INTEGER REFERENCES boulders,
    user_id INTEGER REFERENCES users
);
