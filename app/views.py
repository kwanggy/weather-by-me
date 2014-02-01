import json
import traceback

from flask import *
from functools import update_wrapper

from . import app, db
from .models import User, Session, Post, Tag, getTagXY
from .config import conf
from util import log


def json_response():
    def decorator(f):
        def wrapped():
            try:
                log("args", request.args)
            except:
                pass
            try:
                log("form", request.form)
            except:
                pass
            try:
                res = f()
            except Exception as e:
                log(traceback.format_exc())
                status_code = 404 if request.method == 'GET' else 400
                return jsonify({
                    'status_code': status_code,
                    'error': str(e)
                }), 200 # status_code
            return jsonify({
                'status_code': 200,
                'result': res
            })
        return update_wrapper(wrapped, f)
    return decorator

def session_required():
    def decorator(f):
        def wrapped():
            data = request.args if request.method == 'GET' else request.form
            key = session.get('session_key', None)
            key = data.get('session_key', None) if key == None else key
            if key == None:
                raise Exception('session key is required')

            s = Session.query.filter_by(key=key).first()
            if s == None:
                raise Exception('session was not found')
            if s.owner == None:
                log('****', 'session is not valid', s.id)
                raise Exception('session is not valid')
            return f(s.owner.first())
        return update_wrapper(wrapped, f)
    return decorator

def userinfo_required(create=False):
    def decorator(f):
        def wrapped():
            email = request.form.get('email', None)
            if email == None:
                raise Exception('email address is required')

            pw = request.form.get('pw', None)
            if 'pw' == None:
                raise Exception('password is required')

            if create:
                name = request.form.get('name', None)
                if name == None:
                    raise Exception('name is required')
                pic = request.files.get('pic', None)
                log('pic', pic)

                u = User(email, pw, name)
                db.session.add(u)
                db.session.commit()
                u.setProfilePic(pic)
                db.session.commit()
            else:
                u = User.query.filter_by(email=email).first()
                if u == None:
                    raise Exception('matching email address does not exist')
                if not u.check_password(pw):
                    raise Exception('password does not match')
                s = Session()
                u.set_session(s)
                db.session.add(s)
                db.session.commit()
            return f(u)
        return update_wrapper(wrapped, f)
    return decorator

def newSessionKey(user):
    s = Session()
    user.set_session(s)
    db.session.add(s)
    db.session.commit()
    session['session_key'] = user.session_key
    return dict(session_key=user.session_key)


@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')
    
@app.route('/signin')
def signin_page():
    return render_template('signin.html')
    
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signout')
@session_required()
def signout_page(user):
    user.set_session(None)
    db.session.commit()
    session.pop('session_key', None)
    return redirect(url_for('index_page'))

@app.route('/post')
@session_required()
def post_page(user):
    return render_template('post.html')

@app.route('/api/reset')
@json_response()
def reset():
    try: 
        if not conf['sys']['test']:
            db.engine.execute('DROP TABLE * CASCADE')
        else:
            db.drop_all()
    except Exception as e:
        log('reset', e)
    db.create_all()
    session.pop('session_key', None)
    return len(User.query.all())
    
@app.route('/api/signup', methods=['POST'])
@json_response()
@userinfo_required(create=True)
def api_signup(user):
    return newSessionKey(user)

@app.route('/api/signin', methods=['POST'])
@json_response()
@userinfo_required()
def api_signin(user):
    return newSessionKey(user)

@app.route('/api/post', methods=['GET', 'POST'])
@json_response()
@session_required()
def api_post(user):
    data = request.args if request.method == 'GET' else request.form
    if request.method == 'GET':
        post_id = data.get('post_id', None)
        lat = float(data.get('lat', None))
        lng = float(data.get('lng', None))
        if post_id != None:
            p = Post.query.filter_by(id=post_id).first()
            if p == None:
                raise Exception('post id does not exist')
            res = p.toJson()
        elif lat != None and lng != None:
            x, y = getTagXY(lat, lng)
            p = Tag.query.filter_by(x=x, y=y).first()
            if p == None:
                res = []
            else:
                p = p.posts.all()
                res = [ x.toJson() for x in p ].reverse()
        else:
            raise Exception('post id or (latitude and longitude) is required')
    elif request.method == 'POST':
        text = data.get('text', None)
        if text == None:
            raise Exception('text is required')
        image = request.files.get('image', None)
        if image == None:
            raise Exception('image is required')
        log('image', image)
        lat = float(data.get('lat', None))
        if lat == None:
            raise Exception('latitude is required')
        lng = float(data.get('lng', None))
        if lng == None:
            raise Exception('longitude is required')
        
        p = Post(user, text, lat, lng)
        db.session.add(p)
        db.session.commit()
        p.setImage(image)
        db.session.commit()
        res = p.toJson()
    return res

@app.route('/api/comment', methods=['POST'])
@json_response()
@session_required()
def api_post(user):
    data = request.args if request.method == 'GET' else request.form
    if request.method == 'POST':
        text = data.get('text', None)
        if text == None:
            raise Exception('text is required')
        parent_id = data.get('parent_id', None)
        if parent_id == None:
            raise Exception('parent id is required')
        parent = Post.query.filter_by(id=parent_id).first()
        if parent == None:
            raise Exception('parent not found')
        
        c = Comment(user, parent, text)
        db.session.add(c)
        db.session.commit()
        res = c.toJson()
    return res
