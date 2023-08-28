from flask import request, session
from flask_restful import Resource
from models.activity import formation_list_activity
from models.models import User


class Profile(Resource):
    def get(self):
        data = {'redirect_url': '/profile'}
        data['user_name'] = user.username

        return data



class HomePage(Resource):
    def get(self):
        data = {'redirect_url': '/', 'status':0}
        return data


class UserName(Resource):
    def get(self):
        user = User()
        user = user.get_user(session.get('_user_id'))
        data = {'userName':user.username}
        return data, 200