from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    
    # Подготоваливаем контекст и создаём таблицы
    app.app_context().push()

    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()
