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