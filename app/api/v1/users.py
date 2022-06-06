import logging

from flask import abort, request
from flask_restx import Resource
from marshmallow import ValidationError

from app.api.v1.dto import UserDto
from app.models.roles import RoleSchema
from app.models.users import UserSchema
from app.services.users import get_users_service

from .utils import ok20x

ns = UserDto.ns

ns.logger.setLevel(logging.DEBUG)

user_schema = UserSchema()
user_schema_resp = UserSchema(exclude=["password_hash"])
users_schema = UserSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

api_service = get_users_service()


@ns.route("/<int:id>")
class UsersAPI(Resource):
    @ns.marshal_with(UserDto.user_response)
    def get(
        self,
        id: int,
    ):
        user = api_service.get(id)
        if not user:
            abort(404)
        return user_schema_resp.dump(user)

    def delete(self, id: int):
        result = api_service.delete(id=id)
        if result:
            return ok20x(http_code=204)
        return abort(404)

    def put(self, id):
        try:
            user_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400
        if not api_service.update_user(id, request.json):
            return abort(404)
        return ok20x(http_code=204)


@ns.route("/")
class UsersAPIOther(Resource):
    @ns.expect(UserDto.user_request)
    def post(self):
        try:
            user_schema.load(request.json)
            user = api_service.create(request.json)
        except ValidationError as err:
            return err.messages, 400
        return user_schema_resp.dump(user)


@ns.route("/<int:id>/roles/")
class UsersRolesAPI(Resource):
    @ns.marshal_list_with(UserDto.role_response)
    def get(self, id: int):
        roles = api_service.get_roles(id)
        if not roles:
            abort(404)
        return roles_schema.dump(roles)

    @ns.expect(UserDto.user_roles_req)
    def delete(self, id: int):
        result = api_service.delete_roles(id=id, roles_id=dict(request.json)["ids"])
        if result:
            return ok20x(http_code=204)
        return abort(404)

    @ns.expect(UserDto.user_roles_req)
    def post(self, id: int):

        result = api_service.add_roles(id=id, roles_id=dict(request.json)["ids"])
        if result:
            return ok20x(http_code=201)
        return abort(404)
