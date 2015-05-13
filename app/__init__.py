from flask import Flask

app = Flask(__name__)  # Create the application object of type Flask.
app.config.from_object('config')  # Read and use config file.

from app import views  # At the end to avoid a circular import error.
