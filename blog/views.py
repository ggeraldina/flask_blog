"""This file contains the routings and the view error pages"""
from datetime import datetime

from flask import render_template

from . import app, mongo


@app.route("/")
def post_list():
    posts = mongo.db.blog_post.find({
        "published_date": {"$lt": str(datetime.now().isoformat())}
        }).sort("published_date")
    return render_template('blog/post_list.html', posts=posts)

@app.route("/post/<ObjectId:primary_key>/")
def post_detail(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    return render_template('blog/post_detail.html', post=post)

@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = {"msg": msg}
    return render_template('blog/index.html', data=data), 200

@app.route("/<int:number>")
def show_number(number):
    return "Your number: %d" % number
