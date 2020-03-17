"""This file contains the routings and the view error pages"""
from datetime import datetime

from flask import render_template, request, redirect, url_for

from . import app, mongo


@app.route("/")
def post_list():
    posts = mongo.db.blog_post.find({
        "published_date": {"$lt": str(datetime.utcnow().isoformat())}
        }).sort("published_date")
    return render_template("blog/post_list.html", posts=posts)

@app.route("/post/<ObjectId:primary_key>")
def post_detail(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    return render_template("blog/post_detail.html", post=post)

def save_post(request_post_new, instance_post=None):
    post = {}
    if instance_post:
        post = instance_post
    else:
        post["create_date"] = str(datetime.utcnow().isoformat())
        post["published_date"] = "NULL"
    post["title"] = request_post_new.form.get("title")
    post["text"] = request_post_new.form.get("text")
    post["author"] = "author"
    if instance_post:
        mongo.db.blog_post.update_one({"_id": instance_post["_id"]}, {"$set": post})
    else:
        post["_id"] = mongo.db.blog_post.insert_one(post).inserted_id
    return redirect(url_for("post_detail", primary_key=post["_id"]))

@app.route("/post/new", methods=["GET", "POST"])
def post_new():
    if request.method == "POST":
        return save_post(request)
    else:
        return render_template("blog/post_edit.html")

@app.route("/post/<ObjectId:primary_key>/edit", methods=["GET", "POST"])
def post_edit(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    if request.method == "POST":
        return save_post(request, post)
    else:
        return render_template("blog/post_edit.html", post=post)

@app.route("/drafts")
def post_draft_list():
    posts = mongo.db.blog_post.find({
        "published_date": "NULL"
        }).sort("create_date")
    return render_template("blog/post_draft_list.html", posts=posts)

@app.route("/post/<ObjectId:primary_key>/publish")
def post_publish(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    post["published_date"] = str(datetime.utcnow().isoformat())
    mongo.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
    return redirect(url_for("post_detail", primary_key=primary_key))

@app.route("/post/<ObjectId:primary_key>/remove")
def post_remove(primary_key):
    mongo.db.blog_post.delete_one({"_id": primary_key})
    return redirect(url_for("post_list"))

@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = {"msg": msg}
    return render_template("blog/index.html", data=data)

@app.route("/<int:number>")
def show_number(number):
    return "Your number: %d" % number
