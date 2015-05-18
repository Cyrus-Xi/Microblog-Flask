from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Create the application object of type Flask.
app.config.from_object('config')  # Read and use config file.
db = SQLAlchemy(app)  # Create a db object to be the database.

from app import views, models  # At the end to avoid a circular import error.
