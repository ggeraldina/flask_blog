# -*- coding: utf-8 -*-
from app import app

@app.route("/")
@app.route("/index")
def index():
    return "Hello, world! Привет, мир!"

@app.route("/<int:number>")
def showNumber(number):
    return "Your number: %d" % number