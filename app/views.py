import json
import traceback

from flask import *
from functools import update_wrapper

from . import app, db
# from .models import User, Session
from .config import conf
from util import log


def json_response():
    def decorator(f):
        def wrapped():
            try:
                log(request.args)
            except:
                pass
            try:
                log(request.form)
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
            if request.method == 'GET':
                key = request.args.get('session_key', None)
            elif request.method == 'POST':
                key = request.form.get('session_key', None)
            if key == None:
                raise Exception('session key is required')

            s = Session.query.filter_by(key=key).first()
            if s == None:
                raise Exception('session key is not valid')
            if s.user == None:
                log('****', 'session is not valid', s.id)
                raise Exception('session is not valid')
            return f(s.user.first())
        return update_wrapper(wrapped, f)
    return decorator

def userinfo_required(create=False):
    def decorator(f):
        def wrapped():
            if 'email' not in request.form:
                raise Exception('email address is required')
            eamil = request.form['email']

            if 'pw' not in request.form:
                raise Exception('password is required')
            pw = request.form['pw']

            if 'name' not in request.form:
                raise Exception('name is required')
            name = request.form['name']

            if create:
                u = User(email, pw, name)
                db.session.add(u)
                db.session.commit()
            else:
                u = User.query.filter_by(email=email).first()
                if u == None:
                    raise Exception('matching email address does not exist')
            return f(u)
        return update_wrapper(wrapped, f)
    return decorator

def newSessionKey(user):
    s = Session()
    user.set_session(s)
    db.session.add(s)
    db.session.commit()
    return user.session_key


@app.route('/')
def index_page():
    return render_template('index.html')

