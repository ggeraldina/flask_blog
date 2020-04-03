"""This file contains the routings and the view error pages"""
from datetime import datetime

from flask import redirect, render_template, url_for

from .forms import PostForm

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

@app.route("/post/new", methods=["GET", "POST"])
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = {"create_date": datetime.utcnow().isoformat(),
                "published_date": None,
                "title": form.title.data,
                "text": form.text.data,
                "author": "author"}
        post["_id"] = mongo.db.blog_post.insert_one(post).inserted_id
        return redirect(url_for("post_detail", primary_key=post["_id"]))
    return render_template("blog/post_edit.html", form=form)

@app.route("/post/<ObjectId:primary_key>/edit", methods=["GET", "POST"])
def post_edit(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    form = PostForm(**post)
    if form.validate_on_submit():
        post = {"title": form.title.data,
                "text": form.text.data}
        mongo.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
        return redirect(url_for("post_detail", primary_key=primary_key))
    return render_template("blog/post_edit.html", form=form)

@app.route("/drafts")
def post_draft_list():
    posts = mongo.db.blog_post.find({
        "published_date": None
        }).sort("create_date")
    return render_template("blog/post_draft_list.html", posts=posts)

@app.route("/post/<ObjectId:primary_key>/publish")
def post_publish(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    post["published_date"] = datetime.utcnow().isoformat()
    mongo.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
    return redirect(url_for("post_detail", primary_key=primary_key))

@app.route("/post/<ObjectId:primary_key>/remove")
def post_remove(primary_key):
    mongo.db.blog_post.delete_one({"_id": primary_key})
    return redirect(url_for("post_list"))
