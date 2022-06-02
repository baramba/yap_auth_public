from flask import request
from flask_jwt_extended import get_jwt, jwt_required
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
        user_agent = request.headers.get('User-Agent')
        return users_service.register(register_data, user_agent)


@api.route('/login')
class AuthLogin(Resource):

    auth_login = AuthDto.auth_login

    @api.expect(auth_login)
    def post(self):
        login_data = request.get_json()
        user_agent = request.headers.get('User-Agent')
        return users_service.login(login_data, user_agent)


@api.route('/refresh')
class RefreshToken(Resource):

    @jwt_required(refresh=True)
    def post(self):
        return users_service.refresh()


@api.route('/logout')
class AuthLogout(Resource):

    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token['jti']
        ttype = token['type']
        return users_service.logout(jti, ttype)


@api.route('/change')
class AuthChange(Resource):

    auth_change = AuthDto.auth_change

    @jwt_required()
    @api.expect(auth_change)
    def post(self):
        user_data = request.get_json()
        return users_service.update(user_data)


@api.route('/history')
class AuthHistory(Resource):

    @jwt_required()
    def get(self):
        return users_service.get_history()
