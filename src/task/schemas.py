from pydantic import BaseModel

import uuid
from datetime import datetime

from .models import Priority, Status, Complexity


class TaskCreate(BaseModel):
    title: str = 'Title'
    description: str = 'Description'
    is_active: bool = True
    priority: Priority = Priority.nothing
    status: Status = Status.nothing
    complexity: Complexity = Complexity.nothing
    author: str = 'User'


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    is_active: bool
    priority: Priority
    status: Status
    complexity: Complexity
    author: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskDelete(BaseModel):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    is_active: bool
    priority: Priority
    status: Status
    complexity: Complexity
    author: str

    class Config:
        from_attributes = True
