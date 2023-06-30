from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_restful import Api, Resource
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey123'

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db = SQLAlchemy(app)
app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)
class UserLogin(UserMixin):
    def get_user(self, user_id):
        user = db.session.get(User, user_id)
        return user


    def get_user_from_username(self, username):
        user = db.session.query(User).filter_by(username=username).first()
        return user


# слой модели
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
#окончание слоя модели


api = Api(app)


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

        return {'message': 'Login successful'}, 200

    def get(self):
        if current_user.is_authenticated:
            return {'message': 'User is authenticated'}
        else:
            return {'message': 'User is not authenticated'}, 401



@login_manager.user_loader
def user_loader(user_id):
    return UserLogin.create_user(user_id)


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
        # Обработка POST-запроса
        return {"message": "Received POST request"}


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response


api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')
api.add_resource(DataResource, '/api/data')

if __name__ == '__main__':
    app.run()
