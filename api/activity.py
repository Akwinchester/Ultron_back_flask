from flask import request, session
from flask_restful import  Resource
from models.activity import create_activity, delete_activity, update_activity
from flask import request


class CreateActivity(Resource):
    def post(self):
        activity_name = request.get_json()['name']
        notification_text = request.get_json()['notification_text']
        new_activity_id = create_activity(user_id=session.get('_user_id'), name_activity=activity_name, notification_text=notification_text)

        response = {new_activity_id:activity_name}

        return response, 200


class DeleteActivity(Resource):
    def delete(self, activity_id):
        delete_activity(activity_id)
        return 'Ok', 200


class EditActivity(Resource):
    def post(self, activity_id):
        data_for_update = request.get_json()
        update_activity(data_for_update, activity_id=activity_id)
        return 'Ok', 200

