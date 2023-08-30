from api.pages import UserName

from api.activity import CreateActivity, DeleteActivity, EditActivity
from api.auth import RegisterResource, LogoutResource, LoginResource
from api.chart import DataForChart
from api.entry import DeleteEntry, EditEntry, CreateEntry
from api.pages import Profile, HomePage
from utils import api, login_manager


api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')
api.add_resource(Profile, '/api/Profile')
api.add_resource(HomePage, '/api/home_page')
api.add_resource(DataForChart, '/api/data_for_chart')
api.add_resource(DeleteEntry, '/api/delete_entry/<int:id_entry>')
api.add_resource(EditEntry, '/api/edit_entry/<int:id_entry>')
api.add_resource(CreateEntry, '/api/create_entry/<int:activity_id>')
api.add_resource(CreateActivity, '/api/create_activity')
api.add_resource(DeleteActivity, '/api/delete_activity/<int:activity_id>')
api.add_resource(EditActivity, '/api/edit_activity/<int:activity_id>')
api.add_resource(UserName, '/api/get_username')


def initialize_app(app):
    api.init_app(app)
    login_manager.init_app(app)


    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000, http://95.163.250.203'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
        response.headers['Accept'] = 'application/json'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        return response
