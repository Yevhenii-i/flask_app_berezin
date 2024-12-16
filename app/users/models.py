
import bcrypt
from datetime import datetime as dt
from app import db, login_manager, load_user
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(100), nullable=False)
    about_me = db.Column(db.String(500), nullable=True)
    last_seen =db.Column(db.DateTime, nullable=True, default= dt.now())


    def get_id(self):
        return str(self.id)

    def set_password(self, for_password):
        self.password = bcrypt.generate_password_hash(for_password).decode('utf-8')

    def check_password(self, for_password):
        return bcrypt.check_password_hash(self.password, for_password)

    def __repr__(self):
        return '<User %r>' % self.email