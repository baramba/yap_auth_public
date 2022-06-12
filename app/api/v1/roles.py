from flask import Response, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from marshmallow import ValidationError

from app.api.v1.dto import RolesDto
from app.models.roles import RoleSchema
from app.models.roles_permissions import RolesPermissionsSchema
from app.services.roles import RolesService, get_roles_service

ns = RolesDto.ns


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

role_permissions_schema = RolesPermissionsSchema(many=True)


role_service: RolesService = get_roles_service()


@ns.route("/<int:id>")
class RolesAPI(Resource):
    @ns.marshal_with(RolesDto.role_response)
    @ns.doc(description="Получение данных роли по id")
    @jwt_required()
    def get(self, id: int):
        role = role_service.get(id)
        if not role:
            abort(404)
        return role_schema.dump(role)

    @ns.doc(description="Удаление роли по id")
    @ns.response(204, "Role has been deleted.")
    @ns.response(404, "ID not found.")
    @jwt_required()
    def delete(self, id: int):
        result = role_service.delete(id=id)
        if result:
            return "Role id={0} deleted".format(id), 204
        return abort(404)

    @ns.doc(description="Изменение роли по id")
    @ns.response(204, "Role has been updated.")
    @ns.response(404, "ID not found.")
    @jwt_required()
    def put(self, id):
        try:
            role_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400
        if not role_service.update(id, request.json):
            return abort(404)
        return "Updated role's id={0}.".format(id), 204


@ns.route("/")
class RoleAPI1(Resource):
    @ns.doc(description="Добавление роли")
    @ns.response(201, "Role has been created.")
    @jwt_required()
    @ns.expect(RolesDto.role_response)
    def post(
        self,
    ):
        try:
            role_schema.load(request.json)
            role_id = role_service.create(request.json)
        except ValidationError as err:
            return err.messages, 400
        return "Created role's id={0}.".format(role_id), 201


@ns.route("/<int:id>/permissions")
class RolePermissionsAPI(Resource):
    @ns.doc(description="Добавление прав для роли")
    @ns.response(200, "Permissions has been added to role.")
    @jwt_required()
    @ns.expect(RolesDto.role_permissions_req)
    def post(self, id: int):
        role_service.add_permissions(id, dict(request.json)["ids"])
        return "Add permissions to role.id={0}.".format(id), 200

    @jwt_required()
    @ns.doc(description="Удаление прав у роли")
    @ns.response(200, "Permissions has been deleted from role.")
    @ns.expect(RolesDto.role_permissions_req)
    def delete(self, id: int):
        result = role_service.delete_permissions(id, dict(request.json)["ids"])
        return ("Role id={0} deleted {1} permissions".format(id, result), 200)
