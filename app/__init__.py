from flask import Flask, url_for

app = Flask(__name__, static_folder="static")

from app import routes, errors
