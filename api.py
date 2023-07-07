from flask import request, session
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db
from flask_login import login_user, logout_user, current_user, login_required, login_manager, LoginManager

api = Api()
login_manager = LoginManager()



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

        return {'message': 'Registration successful'}, 201


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
        print(current_user.is_authenticated)
        login_user(user)
        print(current_user.is_authenticated)
        return {'message': 'Перенаправление пользователя'}, 302, {'Location':'/Profile'}

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
        print(current_user.is_authenticated)
        logout_user()
        print(current_user.is_authenticated)
        return {'message': 'Logout successful'}, 302, {'Location':'/home_page'}


class Profile(Resource):
    def get(self):
        data = {"amount": 60, 'activity': 'Подтягивания', 'redirect_url': '/profile'}
        return data

    def post(self):
        data = request.get_json()

        # Обработка POST-запроса
        return {"message": "Received POST request"}


class HomePage(Resource):
    def get(self):
        data = {'redirect_url': '/'}
        return data

    def post(self):
        data = request.get_json()

        # Обработка POST-запроса
        return {"message": "Received POST request"}

api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')
api.add_resource(Profile, '/Profile')
api.add_resource(HomePage, '/home_page')


def initialize_app(app):
    api.init_app(app)
    login_manager.init_app(app)


    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Accept'] = 'application/json'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        return response



    def print_information_after_request():
        print('\033[92m' +
              f'''ВЫПОЛНЯЕТСЯ ПОСЛЕ КАЖДОГО ЗАПРОСА
            Сессия пользователя: {session}
            current_user: {current_user.is_authenticated}'''
              + '\033[0m')


    # @app.before_request
    # def print_information_before_request():
    #     print('----------------------------------------------------------------------------------------------------------')
    #     print('')
    #     print('')
    #     print('\033[94m' +
    #           f'''ВЫПОЛНЯЕТСЯ ПЕРЕД КАЖДЫМ ЗАПРОСОМ
    #         Сессия пользователя: {session}
    #         current_user.is_authenticated: {current_user.is_authenticated}'''
    #           + '\033[0m')
    #     print()