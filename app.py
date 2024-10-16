from flask import Flask, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return '<h1> Hello World! </h1>', 200

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return f"This is your homepage :) - {agent} "

@app.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    year = 2024 - age

    return f"Welcome, {name} - {year}!"

@app.route('/admin')
def admin():
    to_url = "/hi/administrator"
    to_url = url_for("greetings", name="administrator", age=20, _external=True)
    return redirect(to_url)

if __name__ == '__main__':
    app.run()
