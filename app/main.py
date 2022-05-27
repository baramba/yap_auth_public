from flask import Flask

from app.api.v1.ns import blueprint as api_v1
# from app.api.v2.users import blueprint as api_v2
from app.db import init_db

app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.register_blueprint(api_v1)
# app.register_blueprint(api_v2)

init_db(app)


def main():
    app.run()


if __name__ == "__main__":
    main()
