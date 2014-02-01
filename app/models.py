from datetime import datetime
import os
import uuid, OpenSSL

from flask import *
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy


from . import app, db

from .config import conf
from util import totimestamp, sendmail, allowed_file


'''
User have tickets per each ride
'''


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

    def set_session(self, session):
        if self.session:
            db.session.delete(self.session)
        self.session = session

    def check_session(self, key):
        return self.session.key == key

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)
        
    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)

    def new_post(self, title, image, parent=None):
        Post(title, image, self, parent)

    def setProfilePic(self, pic):
        allowed_extensions = conf['upload']['allowed_extensions']
        if pic and allowed_file(pic.filename, allowed_extensions):
            ext = pic.filename.rsplit('.', 1)[1]
            filename = secure_filename('profile_%d.%s' % (self.id, ext))
            path = conf['upload']['upload_folder']
            path = os.path.join(path, 'profile')
            try:
                os.makedirs(path)
            except:
                pass
            path = os.path.join(path, filename)
            pic.save(path)
            self.pic = url_for('static', filename='profile/%s' % filename)
    
    def toJson(self, recursive=False):
        d = dict(
            user_id = self.id,
            created_at = self.created_at,
            email = self.email,
            name = self.name,
            pic = self.pic,
            role = self.role,
        )
        if recursive:
            d['posts'] = [ x.toJson() for x in self.posts.all() ]
        return d
        

class Session(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.key = str(uuid.UUID(bytes = OpenSSL.rand.bytes(16)))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Post(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    author = db.relationship('User',
        backref=db.backref('posts', lazy='dynamic'))
    text = db.Column(db.String)
    image = db.Column(db.String)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) 
    tag = db.relationship('Tag',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, author, text, image, lat, lng):
        self.created_at = datetime.utcnow()
        self.author = author
        self.text = text
        self.setImage(image)
        self.lat = lat
        self.lng = lng
        self.setTag()

    def setImage(self, image):
        exts = conf['upload']['allowed_extensions']
        if image and allowed_file(image.filename, exts):
            ext = image.filename.rsplit('.', 1)[1]
            filename = secure_filename('image_%d.%s' % (self.id, ext))
            path = conf['upload']['upload_folder']
            path = os.path.join(path, 'image')
            try:
                os.makedirs(path)
            except:
                pass
            path = os.path.join(path, filename)
            image.save(path)
            self.image= url_for('static', filename='image/%s' % filename)

    def getTagXY(self):
        n = 3
        loc_a = 40.442767,-86.930378
        loc_b = 40.409575,-86.886604
        w = loc_a[0] - loc_b[0]
        h = loc_a[1] - loc_b[1]
        lat_diff = self.lat - loc_a[0]
        lng_diff = self.lng - loc_a[1]
        x = (int)(lat_diff / (w/n))
        y = (int)(lng_diff / (h/n))
        return (x, y)
        
    def setTag(self):
        x, y = self.getTagXY()
        tag = Tag.query.filter_by(x=x, y=y).first()
        if tag == None:
            tag = Tag(x, y)
        self.tag = tag

    def toJson(self):
        return dict(
            post_id = self.id,
            created_at = self.created_at,
            author = self.author.toJson(False),
            text = self.text,
            image = self.image,
            lat = self.lat,
            lng = self.lng,
            tag = self.tag,
            comments = [ x.toJson() for x in self.comments.all() ],
        )
            


class Comment(db.Model):
    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    author = db.relationship('User',
        backref=db.backref('comments', lazy='dynamic'))
    parent_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent = db.relationship('Post',
        backref=db.backref('comments', lazy='dynamic'))
    text = db.Column(db.String)

    def __init__(self, author, parent, text):
        self.created_at = datetime.utcnow()
        self.author = author
        self.parent = parent
        self.text = text

    def toJson(self):
        return dict(
            comment_id = self.id,
            author = self.author.toJson(False),
            parent_id = self.parent_id,
            text = self.text,
        )
    

db.create_all()
