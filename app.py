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


@app.route("/")
def index():
    movie_list = get_movie_list()
    return render_template("index.html", movies = movie_list)


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

    sql = "SELECT id, username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return redirect("/")
    else:
        return render_template("profile.html", user = user)


@app.route("/movie/<int:id>",methods=["GET"])
def movie(id):

    sql = "SELECT * FROM movies WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    print("movie.user_id"+ str(movie.user_id))
    user = get_user(movie.user_id)
    #print(session["id"])
    #print(user.id)

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
    user_id = session["id"]

    sql = "INSERT INTO movies (name, director, screenwriter, year, description, user_id) VALUES (:name, :director, :screenwriter, :year, :description, :user_id)"
    db.session.execute(sql, {"name":name, "director":director, "screenwriter":screenwriter, "year":year, "description":description, "user_id":user_id})
    db.session.commit()

    return redirect("/")

@app.route("/deletemovie/<int:id>",methods=["POST"])
def deletemovie(id):
    sql = "DELETE FROM movies WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    flash("Deleted successfully")
    return redirect("/")