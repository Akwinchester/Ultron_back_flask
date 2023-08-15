from flask import request
from flask_restful import  Resource
from models.entery import delete_entry, edit_entry, create_entry
from flask import request


class DeleteEntry(Resource):
    def delete(self, id_entry):

        message = delete_entry(id_entry)
        return {'message':message}, 200


class EditEntry(Resource):
    def post(self,  id_entry):
        data_for_edit = request.get_json()
        edit_entry(id_entry=id_entry, data=data_for_edit)

        return 'Ok', 200


class CreateEntry(Resource):
    def post(self,  activity_id):
        data_for_create = request.get_json()
        create_entry(data=data_for_create, activity_id=activity_id)
        return 'Ok', 200