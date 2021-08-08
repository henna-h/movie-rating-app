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
    sql = "SELECT * FROM movies"
    result = db.session.execute(sql)
    return result.fetchall()


@app.route("/")
def index():
    movie_list = get_movie_list()
    return render_template("index.html", movies = movie_list)


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE username=:username"

    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        # TODO: invalid username
        flash("Invalid password or username")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            #correct username and password
            session["username"] = user.username
            session["id"] = user.id
            return redirect("/")
        else:
            #invalid password
            flash("Invalid password or username")
            return redirect("/")



@app.route("/logout")
def logout():
    del session["username"]
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
        session["username"] = username

        return redirect("/")
    
    else:
        flash("This username is taken")
        return redirect("/registration")

@app.route("/profile/<string:username>",methods=["GET"])
def profile(username):

    sql = "SELECT id, username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return redirect("/")
    else:
        return render_template("profile.html", user = user)

def get_user(id):
    sql = "SELECT id, username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user

@app.route("/movie/<int:id>",methods=["GET"])
def movie(id):

    sql = "SELECT * FROM movies WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()

    user = get_user(movie.user_id)

    return render_template("movie.html", movie = movie, user = user)

@app.route("/add-movie",methods=["GET"])
def add_movie_form():

    return render_template("add_movie_form.html")

@app.route("/movie-added",methods=["POST"])
def add_movie():

    name = request.form["name"]
    director = request.form["director"]
    screenwriter = request.form["screenwriter"]
    year = request.form["year"]
    description = request.form["description"]

    sql = "INSERT INTO movies (name, director, screenwriter, year, description) VALUES (:name, :director, :screenwriter, :year, :description)"
    db.session.execute(sql, {"name":name, "director":director, "screenwriter":screenwriter, "year":year, "description":description})
    db.session.commit()

    return redirect("/")