""" The application """
import datetime
import os

from flask import Flask, url_for
from flask_pymongo import PyMongo

APP = Flask(__name__, static_folder="static", instance_relative_config=True) # pylint: disable=invalid-name
APP.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
if "MONGO_URI" in os.environ:
    APP.config["MONGO_URI"] = os.environ["MONGO_URI"]
elif "MONGOLAB_URI" in os.environ:
    APP.config["MONGO_URI"] = os.environ["MONGOLAB_URI"]
APP.permanent_session_lifetime = datetime.timedelta(days=1)
NETLOC = os.environ["NETLOC"]
MONGO = PyMongo(APP)
