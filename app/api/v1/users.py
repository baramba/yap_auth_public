from flask import Blueprint
from flask_restx import Namespace, Resource

api = Namespace("users", "Namespace Description")


@api.route("/")
class Users(Resource):
    def get(self):
        return "Get v1 user {0}".format("v1")
