from flask import request
from flask_jwt_extended.utils import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource

from app.api.v1.dto import AuthDto
from app.services.users import get_users_service

ns = AuthDto.ns

users_service = get_users_service()


@ns.route("/registration")
class AuthRegister(Resource):

    auth_register = AuthDto.auth_register

    @ns.expect(auth_register)
    def post(self):
        register_data = request.get_json()
        user_agent = request.headers.get("User-Agent")
        return users_service.register(register_data, user_agent)


@ns.route("/login")
class AuthLogin(Resource):

    auth_login = AuthDto.auth_login

    @ns.expect(auth_login)
    def post(self):
        login_data = request.get_json()
        user_agent = request.headers.get("User-Agent")
        return users_service.login(login_data, user_agent)


@ns.route("/refresh")
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        return users_service.refresh()


@ns.route("/logout")
class AuthLogout(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        return users_service.logout(jti, ttype)


@ns.route("/change")
class AuthChange(Resource):

    auth_change = AuthDto.auth_change

    @jwt_required()
    @ns.expect(auth_change)
    def post(self):
        user_data = request.get_json()
        return users_service.update(user_data)


@ns.route("/history")
@ns.route("/history/<int:page>")
class AuthHistory(Resource):
    @jwt_required()
    def get(self, page=1):
        return users_service.get_history(page)
