import uuid

from fastapi_users import schemas

from datetime import datetime

from src.user.models import Role


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    first_name: str
    registered_at: datetime
    roles_id: Role


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    first_name: str
    second_name: str
    roles_id: Role
