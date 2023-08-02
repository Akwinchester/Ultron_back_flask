from api.auth import RegisterResource, LogoutResource, LoginResource
from api.chart import DataForChart
from api.entry import DeleteEntry, EditEntry, CreateEntry
from api.pages import Profile, HomePage
from utils import api, login_manager


api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')
api.add_resource(Profile, '/Profile')
api.add_resource(HomePage, '/home_page')
api.add_resource(DataForChart, '/data_for_chart')
api.add_resource(DeleteEntry, '/delete_entry/<int:id_entry>')
api.add_resource(EditEntry, '/edit_entry/<int:id_entry>')
api.add_resource(CreateEntry, '/create_entry/<int:id_activity>')


def initialize_app(app):
    api.init_app(app)
    login_manager.init_app(app)


    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
        response.headers['Accept'] = 'application/json'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        return response