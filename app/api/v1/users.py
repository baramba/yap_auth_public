from flask import abort, request
from flask_restx import Namespace, Resource
from flask_restx import fields as rfields
from marshmallow import ValidationError

from app.db import db
from app.models.users import UserSchema
from app.services.users import get_users_service

ns = Namespace("users", "user API")


user_schema = UserSchema()
# users_schema = UserSchema(many=True)

user_response = ns.model(
    "User",
    {
        "id": rfields.Integer(readonly=True, description="User id number"),
        "first_name": rfields.String(required=True, description="User first name"),
        "last_name": rfields.String(required=True, description="User password"),
        "email": rfields.String(required=True, description="User email"),
    },
)

users_service = get_users_service()


@ns.route("/<int:id>", endpoint="user_ep")
class UsersAPI(Resource):
    @ns.marshal_with(user_response)
    def get(self, id: int):
        user = users_service.get(id)
        if not user:
            abort(404)
        return user_schema.dump(user)

    def delete(self, id: int):
        result = users_service.delete(id=id)
        if result:
            return "User id={0} deleted".format(id), 200
        return abort(404)

    # @ns.expect(user)
    def post(self, id=None):
        try:
            user_schema.load(request.json)
            user_id = users_service.create(request.json)
        except ValidationError as err:
            return err.messages, 400
        return "Created user's id={0}.".format(user_id)

    def put(self, id):
        try:
            user_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400
        if not users_service.update(id, request.json):
            return abort(404)
        return "Updated user's id={0}.".format(id)
