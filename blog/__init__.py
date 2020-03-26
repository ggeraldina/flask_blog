"""The application."""
import os

from flask import Flask, url_for
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder="static", instance_relative_config=True) # pylint: disable=invalid-name
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
if "MONGO_URI" in os.environ:
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]
elif "MONGOLAB_URI" in os.environ:
    app.config["MONGO_URI"] = os.environ["MONGOLAB_URI"]
mongo = PyMongo(app) # pylint: disable=invalid-name
