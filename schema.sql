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

CREATE TABLE walls (
    id SERIAL PRIMARY KEY,
    name TEXT,
    gym_id INTEGER REFERENCES gyms,
    wall_type TEXT
);

CREATE TABLE  boulders (
    id SERIAL PRIMARY KEY,
    wall_id INTEGER REFERENCES walls,
    color TEXT,
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
