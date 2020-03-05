# -*- coding: utf-8 -*-
from . import app

@app.route("/")
@app.route("/index")
def index():
    return "Hello, world! Привет, мир!"