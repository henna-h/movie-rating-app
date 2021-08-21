from flask import Flask
from flask import redirect, render_template, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


def get_movie_list():
    sql = "SELECT * FROM movies ORDER BY submitted_at DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def set_session(user):
    session['id'] = user.id
    session['username'] = user.username

def del_session():
    del session['id']
    del session['username']

def get_user(id):
    sql = "SELECT id, username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user

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




@app.route("/")
def index():
    movie_list = get_movie_list()
    return render_template("index.html", movies = movie_list, get_average_rating = get_average_rating)


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, username, password FROM users WHERE username=:username"

    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)

    if not user:
        #invalid username
        flash("Invalid password or username")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            #correct username and password
            set_session(user)
            return redirect("/")
        else:
            #invalid password
            flash("Invalid password or username")
            return redirect("/")



@app.route("/logout")
def logout():
    del_session()
    return redirect("/")

@app.route("/registration")
def registration_form():
    return render_template("registration_form.html")


@app.route("/register",methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE username=:username"

    result = db.session.execute(sql, {"username":username})
    usernameExists = result.fetchone()

    if not usernameExists:
        hash_value = generate_password_hash(password)

        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()

        sql = "SELECT * FROM users WHERE username=:username"
        result =db.session.execute(sql, {"username":username})
        db.session.commit()
        user = result.fetchone()

        set_session(user)

        return redirect("/")
    
    else:
        flash("This username is taken")
        return redirect("/registration")

@app.route("/profile/<string:username>",methods=["GET"])
def profile(username):

    sqlUser = "SELECT id, username FROM users WHERE username=:username"
    resultUser = db.session.execute(sqlUser, {"username":username})
    user = resultUser.fetchone()

    if not user:
        return redirect("/")
    else:

        sqlReviews = "SELECT * FROM reviews WHERE user_id=:user_id ORDER BY submitted_at DESC"
        resultReviews = db.session.execute(sqlReviews, {"user_id":user.id})
        reviews = resultReviews.fetchall()

        sqlReviewCount = "SELECT COUNT(*) FROM reviews WHERE user_id=:user_id"
        resultReviewCount = db.session.execute(sqlReviewCount, {"user_id":user.id})
        reviewCount = resultReviewCount.fetchone()[0]

        return render_template("profile.html", user = user, reviewCount=reviewCount, reviews = reviews, get_movie=get_movie)


@app.route("/movie/<int:id>",methods=["GET"])
def movie(id):

    sqlMovie = "SELECT * FROM movies WHERE id=:id"
    resultMovie = db.session.execute(sqlMovie, {"id":id})
    movie = resultMovie.fetchone()
    print("movie.user_id"+ str(movie.user_id))

    sqlReviews = "SELECT * FROM reviews WHERE movie_id=:movie_id ORDER BY submitted_at DESC"
    resultReviews = db.session.execute(sqlReviews, {"movie_id":id})
    reviews = resultReviews.fetchall()

    user = get_user(movie.user_id)


    return render_template("movie.html", movie = movie, reviews = reviews, user = user, get_user=get_user, get_average_rating = get_average_rating)

@app.route("/add-movie",methods=["GET"])
def add_movie_form():

    return render_template("add_movie_form.html")

@app.route("/add-review/movie_id?<int:movie_id>",methods=["POST"])
def add_review(movie_id):

    stars = request.form["stars"]
    review = request.form["review"]
    user_id = session["id"]

    sqlReview = "INSERT INTO reviews (stars, review, movie_id, user_id) VALUES (:stars, :review, :movie_id, :user_id)"
    db.session.execute(sqlReview, {"stars":stars, "review":review, "movie_id":movie_id, "user_id":user_id})
    db.session.commit()

    return redirect(url_for("movie", id=movie_id))

@app.route("/movie-added",methods=["POST"])
def add_movie():

    name = request.form["name"]
    director = request.form["director"]
    screenwriter = request.form["screenwriter"]
    cast_members = request.form["cast"]
    year = request.form["year"]
    description = request.form["description"]
    user_id = session["id"]

    sql = "INSERT INTO movies (name, director, screenwriter, cast_members, year, description, user_id) VALUES (:name, :director, :screenwriter, :cast_members, :year, :description, :user_id)"
    db.session.execute(sql, {"name":name, "director":director, "screenwriter":screenwriter, "cast_members":cast_members, "year":year, "description":description, "user_id":user_id})
    db.session.commit()

    return redirect("/")

@app.route("/deletemovie/<int:id>",methods=["POST"])
def deletemovie(id):
    sql = "DELETE FROM movies WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    flash("Deleted successfully")
    return redirect("/")