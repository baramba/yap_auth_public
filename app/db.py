from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:pass@localhost/postgres"
    # Подготоваливаем контекст и создаём таблицы
    app.app_context().push()

    db.init_app(app)
    db.create_all()
