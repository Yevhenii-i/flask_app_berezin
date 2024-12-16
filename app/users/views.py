from . import users_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime

from .forms import LoginForm, RegistrationForm
from .models import User
from .. import db
from flask_login import login_user, logout_user, current_user, login_required

from app import load_user

users_info = [
    {"username" : "admin", "password" : "admin"}
]

@users_bp.route('/account')
@login_required
def get_account():
#    if "username" in session:
    #username = session["username"]
#    user = User.query.filter_by(username=username).first()
    user = current_user
    username = user.username
    id = user.id
    email = user.email
    password = user.password

    return render_template("account.html", username=username, id=id, email=email, password=password)
    #return redirect(url_for("users.login"))

@users_bp.route("/all_accounts")
@login_required
def get_all_accounts():
    users = User.query.all()

    if len(users) == 0:
        return render_template("all_accounts.html", users=users)

    return render_template("all_accounts.html", users=users, count=len(users))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('users.get_account'))

    form1 = LoginForm()
    form2 = RegistrationForm()

    errors1 = [{'field': key, 'messages': form1.errors[key]} for key in form1.errors.keys()] if form1.errors else []
    errors2 = [{'field': key, 'messages': form2.errors[key]} for key in form2.errors.keys()] if form2.errors else []

    for error in errors1+errors2:
        flash(error["messages"], 'danger')

    if request.method == 'POST':
        if request.form.get('action') == 'login' and form1.validate_on_submit():
            email = form1.email.data
            password = form1.password.data
            #remember = form1.remember.data

            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password):
                    login_user(user)
                    #session["username"] = user.username
                    flash("You have successfully logged in.", 'success')
                    return redirect(url_for('users.get_account'))
            else:
                flash("There is no such user", 'danger')

        elif request.form.get('action') == 'register' and form2.validate_on_submit():

            new_user = User(
                username=form2.username.data,
                email=form2.email.data,

            )
            new_user.set_password(form2.password.data)


            db.session.add(new_user)

            db.session.commit()

            print(new_user.id, type(new_user.id))  # Check ID and type
            print(new_user.get_id())

            login_user(new_user)
            flash("Your account has been created", 'success')
            return redirect(url_for('users.get_account'))

    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user in users_info:
            if username == user["username"] and password == user["password"]:
                session["username"] = username
                session["color"] = "success"
                flash("Success: logged in successfully.", "success")
                return redirect(url_for('users.get_profile'))
        flash("Warning: wrong login or password.", "danger")
    """
    return render_template("login.html", form1=form1, form2=form2)

@users_bp.route('/logout')
def logout():
    #session.pop("username", None)
    #session.pop("age", None)
    logout_user()
    flash("You have logged out.", "success")
    return redirect(url_for('users.get_account'))

@users_bp.route('/profile')
def get_profile():
    if "username" in session:
        cookies = []
        for cookie in request.cookies:
            if cookie != 'session':
                cookies.append([cookie, request.cookies[cookie]]) # ім'я, значення
        username_value = session["username"]
        color_value = session["color"]
        return render_template("profile.html", username=username_value, cookies=cookies, color=color_value)
    return redirect(url_for("users.login"))

@users_bp.route('/change_colors', methods=['GET', 'POST'])
def change_colors():
    if request.method == "POST":
        color = request.form["color"]
        session["color"] = color
        return redirect(url_for('users.get_profile'))
    return redirect(url_for('users.get_profile'))


@users_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@users_bp.route('/resume')
def resume():
    return render_template("resume.html")


@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, int)


    return render_template("hi.html", name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = "/hi/administrator"
    to_url = url_for("users.greetings", name="administrator", age=20, _external=True)
    return redirect(to_url)

@users_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'


@users_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response


@users_bp.route('/set_cookie_val', methods=['GET', 'POST'])
def set_cookie_val():
    if request.method == "POST":
        key = request.form["cookie_key"]
        value = request.form["cookie_value"]
        duration = int(request.form["cookie_duration"])
        response = make_response(redirect(url_for('users.get_profile')))
        response.set_cookie(key, value, max_age=duration)
        return response
    return redirect(url_for('users.get_profile'))

@users_bp.route('/delete_cookie_by_key', methods=['GET', 'POST'])
def delete_cookie_by_key():
    if request.method == "POST":
        key = request.form["cookie_key"]
        response = make_response(redirect(url_for('users.get_profile')))
        response.set_cookie(key, '', expires=0)
        return response
    return redirect(url_for('users.get_profile'))

@users_bp.route('/delete_all_cookies', methods=['GET', 'POST'])
def delete_all_cookies():
    if request.method == "POST":
        response = make_response(redirect(url_for('users.get_profile')))
        for cookie in request.cookies:
            if cookie != 'session':
                response.delete_cookie(cookie)
        return response
    return redirect(url_for('users.get_profile'))


@users_bp.route('/get_all_cookies')
def get_all_cookies():
    #cookies = request.cookies.get_dict()
    cookies = 0



