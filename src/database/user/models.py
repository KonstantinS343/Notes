from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Boolean,\
    Column, Table, JSON, MetaData
from sqlalchemy.dialects.postgresql import UUID

import uuid
from datetime import datetime

metadata = MetaData()


roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('username', String, nullable=False, unique=True),
    Column('first_name', String, nullable=False),
    Column('second_name', String),
    Column('email', String, nullable=False, unique=True),
    Column('is_active', Boolean, default=True),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('roles_id', Integer, ForeignKey('roles.id'))
)
