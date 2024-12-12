import bcrypt

from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, for_password):
        self.password = bcrypt.generate_password_hash(for_password).decode('utf-8')

    def check_password(self, for_password):
        return bcrypt.check_password_hash(self.password, for_password)

    def __repr__(self):
        return '<User %r>' % self.email