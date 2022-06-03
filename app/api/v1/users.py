import logging
from typing import Optional

from flask import abort, request
from flask.wrappers import Response
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

from app.models.roles import RoleSchema
from app.models.users import UserSchema
from app.services.users import get_users_service

ns = Namespace("users", "user API")
ns.logger.setLevel(logging.DEBUG)

user_schema = UserSchema()
user_schema_resp = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

api_service = get_users_service()

user_response = ns.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="User id number"),
        "first_name": fields.String(required=True, description="User first name"),
        "last_name": fields.String(required=True, description="User password"),
        "email": fields.String(required=True, description="User email"),
    },
)

user_request = ns.model(
    "User",
    {
        "first_name": fields.String(required=True, description="User first name"),
        "last_name": fields.String(required=True, description="User last name"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)

role_response = ns.model(
    "Role",
    {
        "id": fields.Integer(readonly=True, description="Role id number"),
        "name": fields.String(required=True, description="Role name"),
    },
)

user_roles_req = ns.model(
    "User_roles",
    {
        "ids": fields.List(fields.Integer(required=True, description="Role id"), required=True),
    },
)


def ok20x(response: Optional[str] = None, http_code: int = 200, mimetype="application/json"):
    return Response(response, status=http_code, mimetype=mimetype)


@ns.route("/<int:id>")
class UsersAPI(Resource):
    @ns.marshal_with(user_response)
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
        if not api_service.update(id, request.json):
            return abort(404)
        return ok20x(http_code=204)


@ns.route("/")
class UsersAPIOther(Resource):
    @ns.expect(user_request)
    def post(self):
        try:
            user_schema.load(request.json)
            user = api_service.create(request.json)
        except ValidationError as err:
            return err.messages, 400
        return user_schema_resp.dump(user)


@ns.route("/<int:id>/roles/")
class UsersRolesAPI(Resource):
    @ns.marshal_list_with(role_response)
    def get(self, id: int):
        roles = api_service.get_roles(id)
        if not roles:
            abort(404)
        return roles_schema.dump(roles)

    @ns.expect(user_roles_req)
    def delete(self, id: int):
        result = api_service.delete_roles(id=id, roles_id=dict(request.json)["ids"])
        if result:
            return ok20x(http_code=204)
        return abort(404)

    @ns.expect(user_roles_req)
    def post(self, id: int):
        result = api_service.add_roles(id=id, roles_id=dict(request.json)["ids"])
        if result:
            return ok20x(http_code=201)
        return abort(404)
