import json
import traceback

from flask import *
from functools import update_wrapper

from . import app, db
from .models import User, Session, Post
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
            key = None
            key = session.get('session_key', None)
            session.pop('session_key', None)
            key = key or data.get('session_key', None)
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

            session['session_key'] = u.session_key
            return f(u)
        return update_wrapper(wrapped, f)
    return decorator

def newSessionKey(user):
    s = Session()
    user.set_session(s)
    db.session.add(s)
    db.session.commit()
    return dict(session_key=user.session_key)


@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/signin')
def signin_page():
    return render_template('signin.html')
    
@app.route('/signup')
def signup_page():
    return render_template('signup.html')
    
@app.route('/api/reset')
@json_response()
def reset():
    try: 
        if not conf['sys']['test-mode']:
            db.engine.execute('DROP TABLE "user" CASCADE')
            db.engine.execute('DROP TABLE "session" CASCADE')
            db.engine.execute('DROP TABLE "post" CASCADE')
        else:
            db.drop_all()
    except:
        pass
    db.create_all()
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
        lat = data.get('lat', None)
        lng = data.get('lng', None)
        if post_id == None or lat == None or lng == None:
            raise Exception('post id or (latitude and longitude) is required')
        p = Post.query.filter_by(id=post_id).all()
        p = p.all() if post_id == None else p.first()
        if p == None:
            raise Exception('post id does not exist')
    elif request.method == 'POST':
        text = data.get('text', None)
        if text == None:
            raise Exception('text is required')
        image = data.get('image', None)
        if image == None:
            raise Exception('image is required')
        p = Post(user, text, image)
        db.session.add(p)
        db.session.commit()
    return p.toJson()
