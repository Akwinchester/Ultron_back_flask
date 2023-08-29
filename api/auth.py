from flask import request, make_response, session, redirect
from flask_restful import  Resource
from werkzeug.security import check_password_hash, generate_password_hash

from models.models import User, db
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from utils import login_manager


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Missing required fields'}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 409

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return {'message': 'Перенаправление пользователя'}, 302, {'Location':'/Profile'}
    def get(self):
        return {'message': 'Все окей'},



class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {'message': 'Missing required fields'}, 400

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid username or password'}, 401
        login_user(user)
        # print(session)
        # session_id = session['_id']
        # response = make_response(redirect('/profile'))
        # response.set_cookie('session_id', session_id, samesite='None', secure=True)
        # return response
        return {'message': 'Перенаправление пользователя'}, 302, {'Location':'/api/Profile'}
    def get(self):
        if current_user.is_authenticated:
            return {'message': 'User is authenticated'}
        else:
            return {'message': 'User is not authenticated'}, 401



@login_manager.user_loader
def user_loader(user_id):
    userlogin = User()
    return userlogin.get_user(user_id)


@login_manager.request_loader
def request_loader(request):
    data = request.get_json()
    username = data.get('username')
    user_login = User()
    return user_login.get_user_from_username(username)


class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'message': 'Logout successful'}, 302, {'Location':'/api/home_page'}
