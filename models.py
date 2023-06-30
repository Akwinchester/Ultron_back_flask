from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserLogin(UserMixin):
    def get_user(self, user_id):
        user = db.session.get(User, user_id)
        return user


    def get_user_from_username(self, username):
        user = db.session.query(User).filter_by(username=username).first()
        return user
