from sqlalchemy import String, TIMESTAMP, Column, Enum

from datetime import datetime
import enum

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase


class Role(enum.Enum):
    admin = 'Admin'
    staff = 'Staff'
    user = 'User'


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    roles_id = Column(Enum(Role), default=Role.user)
