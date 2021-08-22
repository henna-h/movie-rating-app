from app import app
import users
import movies
import reviews
from flask import render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    movieList= movies.get_movie_list()
    get_average_rating = movies.get_average_rating

    return render_template("index.html", movies =  movieList, get_average_rating = get_average_rating)


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = users.get_user_by_username(username)

    if not user:
        #invalid username
        flash("Invalid password or username")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            #correct username and password
            users.set_session(user)
            return redirect("/")
        else:
            #invalid password
            flash("Invalid password or username")
            return redirect("/")



@app.route("/logout")
def logout():
    users.del_session()
    return redirect("/")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("registration_form.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        usernameExists = users.get_user_by_username(username)

        if not usernameExists:
            if password == password2:

                hash_value = generate_password_hash(password)

                user = users.register(username, hash_value)

                users.set_session(user)

                return redirect("/")
            else:
                flash("Password fields must match")
                return redirect("/register")
        
        else:
            flash("This username is taken")
            return redirect("/register")

@app.route("/profile/<string:username>",methods=["GET"])
def profile(username):

    user = users.get_user_by_username(username)

    if not user:
        return redirect("/")
    else:

        reviewList = reviews.get_reviews_by_user(user.id)
        reviewCount = reviews.get_users_review_count(user.id)
        moviesSeenList = movies.get_users_seen_movies_list(user.id)
        watchLaterList = movies.get_users_watch_later_list(user.id)
        moviesSeenCount = movies.get_seen_movies_count(user.id)
        watchLaterCount = movies.get_watch_later_count(user.id)

        return render_template("profile.html", user = user, reviewCount=reviewCount, reviews = reviewList, get_movie=movies.get_movie, moviesSeenList = moviesSeenList, watchLaterList = watchLaterList, get_user=users.get_user, moviesSeenCount = moviesSeenCount, watchLaterCount = watchLaterCount)


@app.route("/movie/<int:id>",methods=["GET"])
def movie(id):

    movie = movies.get_movie(id)
    print("movie.user_id"+ str(movie.user_id))

    reviewList = reviews.get_reviews_by_movie(id)

    user = users.get_user(movie.user_id)

    current_user_id = users.get_session_user_id()

    has_been_seen = movies.is_in_seen_list(current_user_id, id)

    is_in_watch_later_list = movies.is_in_watch_later_list(current_user_id, id)

    reviewCount = reviews.get_movies_review_count(id)

    return render_template("movie.html", movie = movie, reviews = reviewList, user = user, get_user=users.get_user, get_average_rating = movies.get_average_rating, has_been_seen = has_been_seen, is_in_watch_later_list = is_in_watch_later_list, reviewCount = reviewCount)

@app.route("/add-movie",methods=["GET", "POST"])
def add_movie():
    if request.method == "GET":
        return render_template("add_movie_form.html")
    else:
        name = request.form["name"]
        director = request.form["director"]
        screenwriter = request.form["screenwriter"]
        cast_members = request.form["cast"]
        year = request.form["year"]
        description = request.form["description"]
        user_id = users.get_session_user_id()

        movies.add_movie(name, director, screenwriter, cast_members, year, description, user_id)

        return redirect("/")


@app.route("/add-review/movie_id?<int:movie_id>",methods=["POST"])
def add_review(movie_id):

    stars = request.form["stars"]
    review = request.form["review"]
    user_id = users.get_session_user_id()

    reviews.add_review(stars, review, user_id, movie_id)

    return redirect(url_for("movie", id=movie_id))


@app.route("/delete-movie/<int:id>",methods=["POST"])
def delete_movie(id):

    movies.delete_movie(id)
    flash("Deleted successfully")
    return redirect("/")

@app.route("/delete-review/<int:id>",methods=["POST"])
def delete_review(id):

    reviews.delete_review(id)
    flash("Review deleted successfully")
    return redirect("/")

@app.route("/movie-seen/<int:movie_id>",methods=["POST"])
def add_movie_to_seen_list(movie_id):

    user_id = users.get_session_user_id()
    movies.mark_movie_as_seen(user_id, movie_id)
    flash("marked as seen")

    return redirect(url_for("movie", id=movie_id))

@app.route("/add-to-watch-later/<int:movie_id>",methods=["POST"])
def add_to_watch_later(movie_id):

    user_id = users.get_session_user_id()
    movies.add_to_watch_later(user_id, movie_id)
    flash("added to your watch later list")

    return redirect(url_for("movie", id=movie_id))

@app.route("/unmark-movie-as-seen/<int:movie_id>",methods=["POST"])
def unmark_as_seen(movie_id):

    user_id = users.get_session_user_id()
    movies.delete_from_seen_list(user_id, movie_id)
    flash("unmarked as seen")

    return redirect(url_for("movie", id=movie_id))

@app.route("/remove-from-watch-later/<int:movie_id>",methods=["POST"])
def remove_from_watch_later(movie_id):

    user_id = users.get_session_user_id()
    movies.delete_from_watch_later_list(user_id, movie_id)
    flash("removed from your watch later list")

    return redirect(url_for("movie", id=movie_id))