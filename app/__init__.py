from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from config import config

login_manager = LoginManager()

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from app.users.models import User
    return User.query.get(user_id)

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.id_attribute = "get_id"
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from . import views

        from .posts import post_bp
        from .users import users_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(users_bp)

    return app

import app.posts.models
import app.users.models