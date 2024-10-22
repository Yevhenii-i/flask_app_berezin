from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def main():  # put application's code here
    return render_template("hello.html")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@app.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, int)


    return render_template("hi.html", name=name, age=age)

@app.route('/admin')
def admin():
    to_url = "/hi/administrator"
    to_url = url_for("greetings", name="administrator", age=20, _external=True)
    return redirect(to_url)

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@app.route('/posts')
def get_posts():

    return render_template("posts.html", posts=posts)

@app.route('/post/<int:post_id>')
def get_post(post_id):
    if id > 3:
        abort(404)
    post = posts[post_id-1]
    return render_template("detail_post.html", post=post)
