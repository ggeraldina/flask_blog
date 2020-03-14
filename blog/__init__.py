"""The application."""
from flask import Flask, url_for
from flask_pymongo import PyMongo


app = Flask(__name__, static_folder="static") # pylint: disable=invalid-name
app.config["MONGO_URI"] = "mongodb://localhost:27017/microblogDB"
mongo = PyMongo(app) # pylint: disable=invalid-name
