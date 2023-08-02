from flask import request, session
from flask_restful import Resource

from models.entery import formation_dataset_for_charts_only_you, formation_dataset_for_charts_rating
from models.activity import formation_list_activity


class DataForChart(Resource):
    def get(self):
        data = formation_list_activity(session.get('_user_id'))

        return data

    def post(self):
        data = request.get_json()

        if data['StatusView'] == False:
            response_data = formation_dataset_for_charts_only_you(data['id'])
        else:
            response_data = formation_dataset_for_charts_rating(data['id'])

        return response_data, 200