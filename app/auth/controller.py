from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.services.users import get_users_service

from .dto import AuthDto

api = AuthDto.api

users_service = get_users_service()


@api.route('/registration')
class AuthRegister(Resource):

    auth_register = AuthDto.auth_register

    @api.expect(auth_register)
    def post(self):
        register_data = request.get_json()
        return users_service.register(register_data)


@api.route('/login')
class AuthLogin(Resource):

    auth_login = AuthDto.auth_login

    @api.expect(auth_login)
    def post(self):
        login_data = request.get_json()
        return users_service.login(login_data)


@api.route('/refresh')
class RefreshToken(Resource):

    @jwt_required(refresh=True)
    def post(self):
        return users_service.refresh()
