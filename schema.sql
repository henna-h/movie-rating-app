CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL, 
    desciption TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL, 
    year INTEGER CHECK (year > 0) NOT NULL, 
    director TEXT NOT NULL, 
    screenwriter TEXT NOT NULL, 
    cast_members TEXT NOT NULL,
    description TEXT NOT NULL, 
    user_id INTEGER REFERENCES users, 
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    stars INTEGER CHECK (stars BETWEEN 1 AND 5) NOT NULL, 
    review TEXT NOT NULL, 
    movie_id INTEGER REFERENCES movies, 
    user_id INTEGER REFERENCES users,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movies_seen (
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies
);

CREATE TABLE watch_later (
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies
);
