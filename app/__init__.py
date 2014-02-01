import urllib

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from util import log, set_log
from config import conf, load_default_conf


load_default_conf()
app = Flask(__name__)
set_log(app.logger.debug)
app.config['DEBUG'] = conf['sys']['debug']
app.config['SECRET_KEY'] = conf['sys']['secret_key']
db = conf['sys']['database']
if db:
    if '://' not in db:
        import os
        db = os.environ[db]
    app.config['SQLALCHEMY_DATABASE_URI'] = db
    db = SQLAlchemy(app)

# add some filters to jinja
app.jinja_env.globals['urlencode'] = urllib.quote_plus

from . import views  
# from . import models, views
