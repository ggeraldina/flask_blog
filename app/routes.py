# -*- coding: utf-8 -*-
from app import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = { "msg": msg }
    return render_template('blog/index.html', data=data), 200

@app.route("/<int:number>")
def showNumber(number):
    return "Your number: %d" % number