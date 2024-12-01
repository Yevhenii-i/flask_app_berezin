from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, jsonify, request, session
from .forms import PostForm
import json

from .models import Post
from .. import db

JSON_FILE = 'posts.json'

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=session.get("username", "Unknown")
        )
        db.session.add(new_post)
        db.session.commit()

        """try:
            # Read existing data from the JSON file
            try:
                with open(JSON_FILE, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            form_data = {
                "title": form.title.data,
                "content": form.content.data,
                "is_active": form.is_active.data,
                "publish_date": form.publish_date.data.strftime('%Y.%m.%d'),
                "category": form.category.data,
                "author": session.get('username', 'Unknown'),
            }

            print(form_data)

            new_id = max((entry.get("id", 0) for entry in data), default=-1) + 1
            form_data["id"] = new_id

            data.append(form_data)
            with open(JSON_FILE, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            return jsonify({"error": str(e)}), 500"""

        return redirect(url_for('.add_post'))
    return render_template('add_post.html', form=form)

@post_bp.route('/')
def get_posts():
    selres = db.select(Post).order_by(Post.posted.desc())  # Select object
    posts = db.session.scalars(selres).all()

    """try:
        with open(JSON_FILE, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []"""
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:post_id>')
def get_post(post_id):

    selres = db.select(Post).where(Post.id == post_id)
    post = db.session.scalar(selres)

    """try:
        with open(JSON_FILE, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    post = posts[post_id]"""
    return render_template("detail_post.html", post=post)

@post_bp.route('/delete/<int:post_id>')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(url_for('.get_posts'))

@post_bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.publish_date = form.publish_date.data
        post.category = form.category.data

        db.session.commit()
        flash("Post updated successfully!")
        return redirect(url_for('.get_posts'))

    return render_template("edit_post.html", form=form, post=post)