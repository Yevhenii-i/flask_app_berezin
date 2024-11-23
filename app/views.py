from flask import request, redirect, url_for, render_template, abort, current_app

#from app import app

@current_app.route('/')
def main():  # put application's code here
    return render_template("hello.html")

@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404