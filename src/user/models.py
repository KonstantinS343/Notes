from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Boolean,\
    Column, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

import uuid
from datetime import datetime


Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    roles_id = Column(Integer, ForeignKey('roles.id'))
