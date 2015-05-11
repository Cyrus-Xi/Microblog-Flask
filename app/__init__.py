from flask import Flask

app = Flask(__name__)  # Create the application object of type Flask.
from app import views  # At the end to avoid a circular import error.
