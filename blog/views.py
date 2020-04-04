""" This file contains the routings and the view pages """
import secrets
from datetime import datetime
from functools import wraps

from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from . import APP, MONGO, NETLOC
from .forms import LoginForm, PostForm, RegistrationForm


@APP.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = MONGO.db.blog_user.find_one({"username": form.username.data})
        if user is None or not check_password_hash(user["password"], form.password.data):
            flash("Неправильное имя или пароль. Пожалуйста, попробуйте еще раз.")
            return redirect(url_for("login"))
        session["logged_in"] = True
        session["username"] = user.get("username", "unknown_user")
        session["superuser"] = user.get("superuser", False)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != NETLOC:
            next_page = url_for("post_list")
        return redirect(next_page)
    return render_template("registration/login.html", form=form)

@APP.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("username", None)
    return redirect(url_for("post_list"))

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Необходимо авторизоваться.")
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return wrapper

def superuser_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("superuser"):
            return abort(404)
        return func(*args, **kwargs)
    return wrapper

@APP.route("/register", methods=["GET", "POST"])
def register():    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {"username": form.username.data,
                "password": generate_password_hash(form.password.data),
                "superuser": False,
                "create_date": datetime.utcnow().isoformat()}
        user["_id"] = MONGO.db.blog_user.insert_one(user).inserted_id
        flash("Поздравляем! Вы успешно зарегистрированы")
        return redirect(url_for("login"))
    return render_template("registration/register.html", form=form)

@APP.route("/admin", methods=["GET", "POST"])
@superuser_required
def superuser_panel():     
    return render_template("registration/superuser_panel.html")

@APP.route("/api/get_userinfo", methods=["GET"])
def get_userinfo():
    login = request.args.get("name")
    if login == "":
        return {"message": "Запрос пуст"}
    attempt_get_login = {"date": datetime.utcnow().isoformat(),
                         "current_user": session.get("username", "unknown_author"),
                         "get_login": login}
    MONGO.db.blog_get_login.insert_one(attempt_get_login)
    user = MONGO.db.blog_user.find_one({"username": login })
    if user is None:
        return {"message": "Пользователя не существует",
                "username": login,}
    return {"message": "Информация по пользователю",
            "username": login,
            "create date": user.get("create_date", "Дата регистрации неизвестна")}


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
                "author": session.get("username", "unknown_author")}
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
    post["published_author"] = session.get("username", "unknown_author")
    MONGO.db.blog_post.update_one({"_id": primary_key}, {"$set": post})
    return redirect(url_for("post_detail", primary_key=primary_key))

@APP.route("/post/<ObjectId:primary_key>/remove")
@login_required
def post_remove(primary_key):
    MONGO.db.blog_post.delete_one({"_id": primary_key})
    return redirect(url_for("post_list"))
