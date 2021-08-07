from flask import Flask
from flask import redirect, render_template, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")


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
            # TODO: correct username and password
            session["username"] = username
            return redirect("/")
        else:
            # TODO: invalid password
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

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return redirect("/")
    else:
        return render_template("profile.html")