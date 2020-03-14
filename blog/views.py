"""This file contains the routings and the view error pages"""
from flask import render_template

from . import app


@app.route("/")
@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = {"msg": msg}
    return render_template('blog/index.html', data=data), 200

@app.route("/<int:number>")
def show_number(number):
    return "Your number: %d" % number
