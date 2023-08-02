from flask_login import LoginManager
from flask_restful import Api

login_manager = LoginManager()

api = Api()

# def initialize_app(app):
#     api.init_app(app)
#     login_manager.init_app(app)
#
#
#     @app.after_request
#     def add_cors_headers(response):
#         response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
#         response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#         response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
#         response.headers['Accept'] = 'application/json'
#         response.headers['Content-Type'] = 'application/json'
#         response.headers['Access-Control-Allow-Credentials'] = 'true'
#
#         return response


