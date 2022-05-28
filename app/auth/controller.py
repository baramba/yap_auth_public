from flask import request
from flask_restx import Resource

from app.services.users import get_users_service

from .dto import AuthDto

api = AuthDto.api

users_service = get_users_service()


@api.route('/registration')
class AuthRegister(Resource):

    auth_register = AuthDto.auth_register

    # @api.expect(auth_register)
    def post(self):
        register_data = request.get_json()
        return users_service.create(register_data)
