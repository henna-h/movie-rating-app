CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);

CREATE TABLE movies (id SERIAL PRIMARY KEY, name TEXT UNIQUE, year INTEGER, director TEXT, screenwriter TEXT, description TEXT, user_id INTEGER REFERENCES users, submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE cast_members(id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE cast_members_of_a_movie(cast_member_id INTEGER REFERENCES cast_members, movie_id INTEGER REFERENCES movies)

CREATE TABLE reviews (id SERIAL PRIMARY KEY, stars INTEGER, review TEXT, movie_id INTEGER REFERENCES movies, user_id INTEGER REFERENCES users);

