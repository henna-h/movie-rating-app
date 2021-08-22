from operator import truediv
from db import db

def get_movie_list():
    sql = "SELECT * FROM movies ORDER BY submitted_at DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_movie(id):
    sql = "SELECT * FROM movies WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    return movie

def get_average_rating(movie_id):
    sql = "SELECT ROUND(AVG(stars), 1) FROM reviews WHERE movie_id=:id"
    result = db.session.execute(sql, {"id":movie_id})
    average = result.fetchone()[0]

    return average

def add_movie(name, director, screenwriter, cast_members, year, description, user_id):

    sql = "INSERT INTO movies (name, director, screenwriter, cast_members, year, description, user_id) VALUES (:name, :director, :screenwriter, :cast_members, :year, :description, :user_id)"
    db.session.execute(sql, {"name":name, "director":director, "screenwriter":screenwriter, "cast_members":cast_members, "year":year, "description":description, "user_id":user_id})
    db.session.commit()

def delete_movie(id):

    sqlReviews = "DELETE FROM reviews WHERE movie_id=:id"
    db.session.execute(sqlReviews, {"id":id})
    db.session.commit()

    sqlMovie = "DELETE FROM movies WHERE id=:id"
    db.session.execute(sqlMovie, {"id":id})
    db.session.commit()

def mark_movie_as_seen(user_id, movie_id):
    sql = "INSERT INTO movies_seen (user_id, movie_id) VALUES (:user_id, :movie_id)"
    db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    db.session.commit()

def add_to_watch_later(user_id, movie_id):
    sql = "INSERT INTO watch_later (user_id, movie_id) VALUES (:user_id, :movie_id)"
    db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    db.session.commit()

def is_in_seen_list(user_id, movie_id):
    sql="SELECT COUNT(*) FROM movies_seen WHERE user_id=:user_id AND movie_id=:movie_id"
    result = db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    count = result.fetchone()[0]

    if count > 0:
        return True
    else:
        return False

def is_in_watch_later_list(user_id, movie_id):
    sql="SELECT COUNT(*) FROM watch_later WHERE user_id=:user_id AND movie_id=:movie_id"
    result = db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    count = result.fetchone()[0]

    if count > 0:
        return True
    else:
        return False

def delete_from_seen_list(user_id, movie_id):
    sql="DELETE FROM movies_seen WHERE user_id=:user_id AND movie_id=:movie_id"
    db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    db.session.commit()

def delete_from_watch_later_list(user_id, movie_id):
    sql="DELETE FROM watch_later WHERE user_id=:user_id AND movie_id=:movie_id"
    db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    db.session.commit()

def get_users_seen_movies_list(user_id):
    sql = "SELECT movie_id FROM movies_seen WHERE user_id=:user_id"
    result =db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    movieList = result.fetchall()
    print(str(movieList))

    return movieList

def get_users_watch_later_list(user_id):
    sql = "SELECT movie_id FROM watch_later WHERE user_id=:user_id"
    result =db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    movieList = result.fetchall()

    return movieList