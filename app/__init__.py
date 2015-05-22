import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)  # Create the application object of type Flask.
app.config.from_object('config')  # Read and use config file.
db = SQLAlchemy(app)  # Create a db object to be the database.
lm = LoginManager()
lm.init_app(app)
# Tell Flask-Login which view logs users in.
lm.login_view = 'login'
# Flask-OpenID needs a temp folder.
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models  # At the end to avoid a circular import error.
