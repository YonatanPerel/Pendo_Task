from flask import Flask, g, session
from passlib.hash import pbkdf2_sha256
from .DB_Access import add_user, search_user


def create_new_user(user_name, password):
    password = hash_password(password)
    if search_user(user_name):
        return "UserAlreadyExists"
    add_user(user_name, password)
    connect_user(user_name)
    return ''


def verify_user(user_name, password):
    db_password = search_user(user_name)
    print(db_password)
    if 'password' in db_password:
        if(verify_password(password, db_password['password'])):
            connect_user(user_name)
            return ''
    disconnect_user()
    return "UserNotFound"


def hash_password(password):
    print (pbkdf2_sha256.hash(password))
    return pbkdf2_sha256.hash(password)


def verify_password(password, hash):
    print (hash)
    return pbkdf2_sha256.verify(password, hash)


def connect_user(user_name):
    """this connects a user. DO NOT use this without varefiying the user first."""
    session['username'] = user_name
    session['logged_in'] = True

def disconnect_user():
    session['username'] = ''
    session['logged_in'] = False
