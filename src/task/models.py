from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

import uuid
import enum
from datetime import datetime

from src.user.models import User


Base = declarative_base()


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


class Note(Base):
    __tablename__ = 'notes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Enum(Priority), default='Nothing')
    status = Column(Enum(Status), default='Nothing')
    complexity = Column(Enum(Complexity), default='Nothing')
    author = Column(String, ForeignKey(User.username), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
