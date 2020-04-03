""" This file contains the routings and the view pages """
import secrets
from datetime import datetime
from functools import wraps

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.urls import url_parse

from . import APP, MONGO, NETLOC
from .forms import LoginForm, PostForm


@APP.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and secrets.compare_digest(form.password.data, "admin"):
            session["logged_in"] = True
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != NETLOC:
                next_page = url_for("post_list")
            return redirect(next_page)
        flash("Неправильное имя или пароль. Пожалуйста, попробуйте еще раз.")
    return render_template("registration/login.html", form=form)

@APP.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("post_list"))

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Необходимо авторизоваться.")
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return wrapper

@APP.route("/")
def post_list():
    posts = MONGO.db.blog_post.find({
        "published_date": {"$lt": datetime.utcnow().isoformat()}
    }).sort("published_date")
    return render_template("blog/post_list.html", posts=posts)

@APP.route("/post/<ObjectId:primary_key>")
def post_detail(primary_key):
    post = MONGO.db.blog_post.find_one_or_404({"_id": primary_key})
    return render_template("blog/post_detail.html", post=post)

@APP.route("/post/new", methods=["GET", "POST"])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = {"create_date": datetime.utcnow().isoformat(),
                "published_date": None,
                "title": form.title.data,
                "text": form.text.data,
                "author": "author"}
        post["_id"] = MONGO.db.blog_post.insert_one(post).inserted_id
        return redirect(url_for("post_detail", primary_key=post["_id"]))
    return render_template("blog/post_edit.html", form=form)

@APP.route("/post/<ObjectId:primary_key>/edit", methods=["GET", "POST"])
@login_required
def post_edit(primary_key):
    post = MONGO.db.blog_post.find_one_or_404({"_id": primary_key})
    form = PostForm(**post)
    if form.validate_on_submit():
        post = {"title": form.title.data,
                "text": form.text.data}
        MONGO.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
        return redirect(url_for("post_detail", primary_key=primary_key))
    return render_template("blog/post_edit.html", form=form)

@APP.route("/drafts")
@login_required
def post_draft_list():
    posts = MONGO.db.blog_post.find({
        "published_date": None
        }).sort("create_date")
    return render_template("blog/post_draft_list.html", posts=posts)

@APP.route("/post/<ObjectId:primary_key>/publish")
@login_required
def post_publish(primary_key):
    post = MONGO.db.blog_post.find_one_or_404({"_id": primary_key})
    post["published_date"] = datetime.utcnow().isoformat()
    MONGO.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
    return redirect(url_for("post_detail", primary_key=primary_key))

@APP.route("/post/<ObjectId:primary_key>/remove")
@login_required
def post_remove(primary_key):
    MONGO.db.blog_post.delete_one({"_id": primary_key})
    return redirect(url_for("post_list"))
