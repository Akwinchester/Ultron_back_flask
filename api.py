from flask import request
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db, UserLogin
from flask_login import login_user, logout_user, current_user, login_required, login_manager, LoginManager

api = Api()
login_manager = LoginManager()


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'message': 'Missing required fields'}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 409

        new_user = User(username=username, email=email, password=generate_password_hash(password))
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

        login_user(user)

        return {'message': 'Перенаправление пользователя', 'redirect_url': '/Profile'}, 302, {'Location': '/Profile'}

    def get(self):
        if current_user.is_authenticated:
            return {'message': 'User is authenticated'}
        else:
            return {'message': 'User is not authenticated'}, 401



@login_manager.user_loader
def user_loader(user_id):
    userlogin = UserLogin()
    return userlogin.get_user(user_id)


@login_manager.request_loader
def request_loader(request):
    data = request.get_json()
    username = data.get('username')
    user_login = UserLogin()
    return user_login.get_user_from_username(username)


class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'message': 'Logout successful'}, 200


class DataResource(Resource):
    def get(self):
        data = {"message": "салам"}
        return data

    def post(self):
        data = request.get_json()
        print(data)
        # Обработка POST-запроса
        return {"message": "Received POST request"}


api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')
api.add_resource(DataResource, '/api/data')


def initialize_app(app):
    api.init_app(app)
    login_manager.init_app(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        return response
