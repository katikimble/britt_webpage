"""
File:  poetry_app/models.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the database models for the Poetry App, including User, Poem, AboutMe, Art, and Subscriber models.
- These models represent the structure of the database tables and include fields and methods related to the app's core
functionalities.
"""

from datetime import datetime
from poetry_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    '''User model'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # One user to many poems
    poems = db.relationship('Poem', backref='author', lazy='dynamic')

    def __init__(self, username, email, password_hash, is_admin=False):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.is_admin}')"


class Poem(db.Model):
    '''Poem model'''
    __tablename__ = 'poems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    background = db.Column(db.String(255), nullable=True)

    def __init__(self, title, content, user_id, background=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.background = background

    def __repr__(self):
        return f"Poem('{self.title}', '{self.date_posted}')"


class AboutMe(db.Model):
    '''AboutMe model'''
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)


class Art(db.Model):
    '''Poem model'''
    __tablename__ = 'art'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    art_upload = db.Column(db.String(255), nullable=True)

    def __init__(self, title, art_upload=None):
        self.title = title
        self.art_upload = art_upload

    def __repr__(self):
        return f"Art('{self.title}', '{self.date_posted}')"


class Subscriber(db.Model):
    '''Subscriber model'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

