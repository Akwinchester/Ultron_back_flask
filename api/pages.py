from flask import request, session
from flask_restful import Resource
from models.activity import formation_list_activity
from models.models import User


class Profile(Resource):
    def get(self):
        data = {'redirect_url': '/profile'}
        user = User()
        user = user.get_user(session.get('_user_id'))
        data['user_name'] = user.username
        # data.update(formation_list_activity(56))
        return data



class HomePage(Resource):
    def get(self):
        data = {'redirect_url': '/', 'status':0}
        return data

