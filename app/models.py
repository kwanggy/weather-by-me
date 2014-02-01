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


def writeFile(filename, bytes):
    pass


class User(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    pw_hash = db.Column(db.String)
    name = db.Column(db.String)
    pic = db.Column(db.String)
    session_key = db.Column(db.String, db.ForeignKey('session.key'))
    session = db.relationship('Session',
        backref=db.backref('owner', lazy='dynamic'))
    role = db.Column(db.String)

    def __init__(self, email, pw, name, role=None):
        self.created_at = datetime.utcnow()
        self.email = email
        self.set_password(pw)
        self.name = name
        self.session = None
        self.role = role

    def make_session(self):
        if self.session != None:
            db.session.delete(self.session)
        self.session = Session()

    def set_session(self, session):
        if self.session:
            db.session.delete(self.session)
        self.session = Session()

    def check_session(self, key):
        return self.session.key == key

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)
        
    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)

    def new_post(self, title, image, parent=None):
        Post(title, image, self, parent)

    def setProfilePic(self, pic):
        filename = 'profile_%d.png' % self.id
        writeFile(filename, pic)
        self.pic = '/static/%s' % filename
        

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
    author_id = db.Column(db.String, db.ForeignKey('user.id')) 
    author = db.relationship('User',
        backref=db.backref('posts', lazy='dynamic'))
    text = db.Column(db.String)
    image = db.Column(db.String)

    def __init__(self, author, text, image):
        self.created_at = datetime.utcnow()
        self.author = author
        self.text = text
        self.image = image


class Comment(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.String, db.ForeignKey('user.id')) 
    author = db.relationship('User',
        backref=db.backref('comments', lazy='dynamic'))
    post_id = db.Column(db.String, db.ForeignKey('post.id'))
    post = db.relationship('Post',
        backref=db.backref('comments', lazy='dynamic'))
    text = db.Column(db.String)

    def __init__(self, author, post, text):
        self.created_at = datetime.utcnow()
        self.author = author
        self.post = post
        self.text = text
    

db.create_all()
