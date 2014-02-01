from datetime import datetime
import uuid, OpenSSL

from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy


from . import app, db

from util import totimestamp, sendmail


'''
User have tickets per each ride
'''


class User(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    pw = db.Column(db.String)
    name = db.Column(db.String)
    session = db.relationship('Session', backref='owner', lazy='dynamic')
    role = db.Column(db.String)

    def __init__(self, email, pw, name, role=None):
        self.created_at = datetime.utcnow()
        self.email = email
        self.pw = pw
        self.name = name
        self.role = role

        self.set_session()

    def make_session(self):
        if self.session != None:
            db.session.delete(self.session)
        self.session = Session()

    def set_session(self, session):
        if self.session:
            db.session.delete(self.session)
        self.session = session

    def check_session(self, key):
        return self.session.key == key

    def new_post(title, image, parent=None):
        Post(title, image, self, parent)
        

class Session(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.key = str(uuid.UUID(bytes = OpenSSL.rand.bytes(16)))

class Post(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    author = db.relationship('User', backref='posts', lazy='dynamic')
    parent = db.relationship('Post', backref='comments', lazy='dynamic')

    def __init__(self, title, image, author, parent=None):
        self.created_at = datetime.utcnow()
        self.title = title
        self.image = image
        self.author = author
        self.parent = parent
    

db.create_all()
