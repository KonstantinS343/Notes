from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import uuid

from src.database import get_db
from src.task.models import Note
from .schemas import TaskCreate, TaskResponse


router = APIRouter(
    prefix='/api/v1/task',
    tags=['Task']
)


@router.get('/', response_model=TaskResponse)
async def get_all_task(session: AsyncSession = Depends(get_db)) -> TaskResponse:
    query = select(Note).where(Note.is_active == True)

    result = await session.execute(query)
    result = result.scalars().all()

    result_in_dict = result[0].__dict__
    del result_in_dict['_sa_instance_state']

    return result_in_dict


@router.post('/', response_model=TaskResponse)
async def create_new_task(create_scheme: TaskCreate, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    new_task = Note(**create_scheme.dict())

    session.add(new_task)
    await session.commit()

    return new_task


@router.get('/{note_id}', response_model=TaskResponse)
async def get_note_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    query = select(Note).where(Note.id == note_id)

    result = await session.execute(query)
    result = result.scalars().all()

    result_in_dict = result[0].__dict__
    del result_in_dict['_sa_instance_state']

    return result_in_dict


@router.delete('/{note_id}', response_model=TaskResponse)
async def get_note_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    pass


@router.put('/{note_id}', response_model=TaskResponse)
async def get_note_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    pass


@router.patch('/{note_id}', response_model=TaskResponse)
async def get_note_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    pass
