from datetime import datetime

from app.db import db


class UsersHistory(db.Model):
    __tablename__ = "users_history"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_agent = db.Column(db.String(150), nullable=False)
    auth_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UsersHistory {self.id} {self.user_id} {self.user_agent} {self.auth_date}>"
