from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="Authenticate and receive tokens.")

    auth_register = api.model(
        "Registration data",
        {
            "first_name": fields.String(description="User first name"),  # Optional
            "last_name": fields.String(description="User password"),  # Optional
            "email": fields.String(required=True, description="User email"),
            "password": fields.String(required=True, description="User password"),
        },
    )
