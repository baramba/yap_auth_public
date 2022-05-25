from flask import Flask

from app.api.v1.ns import blueprint as apiv1
from app.api.v2.users import users as usersv2
from app.db import init_db

app = Flask(__name__)


# app.register_blueprint(usersv1, url_prefix="/api/v1")
app.register_blueprint(usersv2, url_prefix="/api/v2")
app.register_blueprint(apiv1)


def main():
    init_db(app)
    app.run()


if __name__ == "__main__":
    main()
