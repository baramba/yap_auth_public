from pydantic import BaseModel


class MetaBaseModel(BaseModel):
    id: int = -1


class User(MetaBaseModel):
    first_name: str
    last_name: str
    password: str
    email: str


class Role(MetaBaseModel):
    name: str


class Permission(MetaBaseModel):
    name: str
