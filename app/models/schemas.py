from app import ma


class UserHistory(ma.Schema):
    class Meta:
        fields = ("user_agent", "auth_date")
