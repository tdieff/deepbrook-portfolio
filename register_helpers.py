import re

from flask import redirect, render_template, request, session
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect('finance.db') 


def username_declared():
    if not request.form.get("username"):
        return False
    else:
        return True


def username_available():
    entries = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    if len(entries) > 0:
        return False
    else:
        return True


def password_declared():
    if not request.form.get("password"):
        return False
    else:
        return True


def password_retyped():
    if not request.form.get("confirmation"):
        return False
    else:
        return True


def validate_length(password):
    if len(password) < 8:
        return False
    else:
        return True


def contains_number(password):
    if re.match(".*\\d.*", password) == None:
        return False
    else:
        return True


def contains_symbol(password):
    if any(not c.isalnum() for c in password) == False:
        return False
    else:
        return True


def passwords_match(password):
    if password != request.form.get("confirmation"):
        return False
    else:
        return True


def validate_password():
    password = request.form.get("password")
    if validate_length(password) == False:
        return False
    elif contains_number(password) == False:
        return False
    elif contains_symbol(password) == False:
        return False
    elif passwords_match(password) == False:
        return False
    else:
        return True


def get_hash():
    return generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)


def insert_user():
    hashed_password = get_hash()
    username = request.form.get("username")
    db.execute("INSERT INTO users (id, username, hash) VALUES (NULL, :username, :hashed_password)", username=username, hashed_password=hashed_password)
    return