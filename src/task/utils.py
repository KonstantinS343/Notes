from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, and_

import uuid
from typing import Union

from src.task.models import Note
from .schemas import TaskCreate, TaskResponse, TaskDelete, TaskUpdate


async def _execute_get_request(query, session: AsyncSession) -> Union[TaskResponse, None]:
    result = await session.execute(query)
    result = result.scalars().all()

    return result


async def _get_active_tasks(session: AsyncSession, username: str) -> Union[TaskResponse, None]:
    query = select(Note).where(and_(Note.is_active == True, Note.author == username))

    return await _execute_get_request(query, session)


async def _get_task_by_id(note_id: uuid.UUID, session: AsyncSession, username: str) -> Union[TaskResponse, None]:
    query = select(Note).where(and_(Note.id == note_id, Note.is_active == True, Note.author == username))

    return await _execute_get_request(query, session)


async def _delete_active_task(note_id: uuid.UUID, session: AsyncSession, username: str) -> Union[TaskDelete, None]:
    query = (
        update(Note)
        .where(and_(Note.id == note_id, Note.is_active == True, Note.author == username))
        .values(is_active=False)
        .returning(Note.id, Note.is_active)
    )

    result = await session.execute(query)
    result = result.all()
    await session.commit()

    return result


async def _create_new_task(create_scheme: TaskCreate, session: AsyncSession) -> Union[TaskResponse, None]:
    new_task = Note(**create_scheme.dict())

    session.add(new_task)
    await session.commit()

    return new_task


async def _update_task(create_scheme: TaskCreate, note_id: uuid.UUID, session: AsyncSession, username: str) -> Union[TaskUpdate, None]:
    create_scheme = create_scheme.dict()
    query = (
        update(Note)
        .where(and_(Note.id == note_id, Note.is_active == True, Note.author == username))
        .values(create_scheme)
        .returning(
            Note.id,
            Note.title,
            Note.description,
            Note.is_active,
            Note.priority,
            Note.status,
            Note.complexity,
            Note.author)
    )
    try:
        result = await session.execute(query)
        result = result.all()
        await session.commit()
    except IntegrityError:
        return None

    return result


async def _partial_update_task(create_scheme: TaskCreate, note_id: uuid.UUID, session: AsyncSession, username: str) -> Union[TaskResponse, None]:
    user_data = create_scheme.dict(exclude_defaults=True)
    query = (
        update(Note)
        .where(and_(Note.id == note_id, Note.is_active == True, Note.author == username))
        .values(user_data)
        .returning(
            Note.id,
            Note.title,
            Note.description,
            Note.is_active,
            Note.priority,
            Note.status,
            Note.complexity,
            Note.author)
    )
    print(query)
    try:
        result = await session.execute(query)
        result = result.all()
        await session.commit()
    except IntegrityError:
        return None

    return result
