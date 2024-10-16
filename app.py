from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
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

    return f"Welcome, {name} - {age}!"


if __name__ == '__main__':
    app.run()
