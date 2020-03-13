from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = {"msg": msg}
    return render_template('blog/index.html', data=data), 200

@app.route("/<int:number>")
def show_number(number):
    return "Your number: %d" % number
