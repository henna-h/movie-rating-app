from db import db
from flask import  session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

def set_session(user):
    session['id'] = user.id
    session['username'] = user.username

def get_session_user_id():
    return session['id']

def del_session():
    del session['id']
    del session['username']

def get_user(id):
    sql = "SELECT id, username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user

def get_user_by_username(username):
    sql = "SELECT id, username, password FROM users WHERE username=:username"

    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    return user

def register(username, hash_value):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    sql = "SELECT * FROM users WHERE username=:username"
    result =db.session.execute(sql, {"username":username})
    db.session.commit()
    user = result.fetchone()

    return user
