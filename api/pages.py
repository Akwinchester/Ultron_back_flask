from flask import request
from flask_restful import Resource
from models.activity import formation_list_activity



class Profile(Resource):
    def get(self):
        data = {'redirect_url': '/profile'}
        data.update(formation_list_activity(56))
        return data



class HomePage(Resource):
    def get(self):
        data = {'redirect_url': '/', 'status':0}
        return data

