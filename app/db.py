from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_db(app: Flask):

    # Подготоваливаем контекст и создаём таблицы
    app.app_context().push()

    db.init_app(app)
    # Migrate(app, db)
    db.create_all()
