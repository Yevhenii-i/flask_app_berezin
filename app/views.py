from flask import request, redirect, url_for, render_template, abort
from app import app

@app.route('/')
def main():  # put application's code here
    return render_template("hello.html")
