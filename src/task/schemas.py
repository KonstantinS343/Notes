from pydantic import BaseModel

import uuid
from datetime import datetime

from .models import Priority, Status, Complexity


class TaskCreate(BaseModel):
    title: str
    description: str
    is_active: bool
    priority: Priority
    status: Status
    complexity: Complexity
    author: str


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
        orm_mode = True
