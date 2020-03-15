"""This file contains the routings and the view error pages"""
from datetime import datetime

from flask import render_template, request

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

# def save_post(request_post_new, instance_post=None):
#     form = PostForm(request_post_new.POST, instance=instance_post)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request_post_new.user
#         post.save()
#         return render_template('post_detail', primary_key=post._id)

@app.route("/post/<ObjectId:primary_key>/edit/", methods=['GET', 'POST'])
def post_edit(primary_key):
    post = mongo.db.blog_post.find_one_or_404({"_id": primary_key})
    return render_template('blog/post_edit.html', post=post)
    # if request.method == "POST":
    #     return save_post(request, post)
    # else:
    #     form = PostForm(instance=post)
    #     return render_template('blog/post_edit.html', form=form)



@app.route("/index")
def index():
    msg = "Привет, замечательный человек!!!"
    data = {"msg": msg}
    return render_template('blog/index.html', data=data), 200

@app.route("/<int:number>")
def show_number(number):
    return "Your number: %d" % number
