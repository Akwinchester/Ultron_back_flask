from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import session

db = SQLAlchemy()


user_activity = db.Table('user_activity',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                         db.Column('activity_id', db.Integer, db.ForeignKey('activity.id'), primary_key=True)
                         )

user_friend = db.Table('user_friend',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    chat_id = db.Column(db.String(50))

    password = db.Column(db.String(128), nullable=False)
    activities = db.relationship('Activity', secondary='user_activity', backref=db.backref('users', lazy='dynamic'))

    nick = db.Column(db.String(50), default='')

    friends = db.relationship('User',
                              secondary='user_friend',
                              primaryjoin=(id == user_friend.c.user_id),
                              secondaryjoin=(id == user_friend.c.friend_id),
                              backref=db.backref('user_friends', lazy='dynamic'), lazy='dynamic')

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)

    def remove_friend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def is_authenticated(self):
        return '_user_id' in session

    def get_user(self, user_id):
        user = db.session.get(User, user_id)
        return user

    def get_user_from_username(self, username):
        user = db.session.query(User).filter_by(username=username).first()
        return user



class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_text = db.Column(db.String(500), default='')


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(300), default='')
    date_added = db.Column(db.Date)

