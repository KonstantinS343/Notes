from sqlalchemy import Table, Column, String, Boolean, Enum, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid
import enum

from src.user.models import users

metadata = MetaData()


class Priority(enum.Enum):
    nothing = 'Nothing'
    low = 'Low'
    medium = 'Medium'
    urgent = 'Urgent'


class Status(enum.Enum):
    nothing = 'Nothing'
    started = 'Started'
    in_progress = 'In process'
    in_review = 'In review'
    done = 'Done'


class Complexity(enum.Enum):
    nothing = 'Nothing'
    low = 'Low'
    medium = 'Medium'
    hard = 'Hard'
    extreme = 'Extreme'


notes = Table(
    'notes',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('is_active', Boolean, default=True),
    Column('priority', Enum(Priority), default='Nothing'),
    Column('status', Enum(Status), default='Nothing'),
    Column('complexity', Enum(Complexity), default='Nothing'),
    Column('author', UUID, ForeignKey(users.c.id), nullable=False)
)
