from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

import uuid
from typing import List

from src.database import get_db
from .schemas import TaskCreate, TaskResponse, TaskDelete, TaskUpdate
from .utils import _get_active_tasks, _get_task_by_id, _create_new_task, \
    _delete_active_task, _update_task, _partial_update_task


router = APIRouter(
    prefix='/api/v1/task',
    tags=['Task']
)


@router.get('/', response_model=List[TaskResponse])
async def get_all_task(session: AsyncSession = Depends(get_db)) -> List[TaskResponse]:
    response = await _get_active_tasks(session=session)

    if not response:
        raise HTTPException(status_code=404, detail='No tasks')

    return response


@router.post('/', response_model=TaskResponse)
async def create_new_task(create_scheme: TaskCreate, session: AsyncSession = Depends(get_db)) -> TaskResponse:
    response = await _create_new_task(create_scheme=create_scheme, session=session)

    return response


@router.get('/{note_id}', response_model=List[TaskResponse])
async def get_task_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> List[TaskResponse]:
    response = await _get_task_by_id(note_id=note_id, session=session)

    if not response:
        raise HTTPException(status_code=404, detail='No such task was found')

    return response


@router.delete('/{note_id}', response_model=List[TaskDelete])
async def delete_task_by_id(note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> List[TaskDelete]:
    response = await _delete_active_task(note_id=note_id, session=session)

    if not response:
        raise HTTPException(status_code=404, detail='No such task was found')

    return response


@router.put('/{note_id}', response_model=List[TaskUpdate])
async def update_task_by_id(create_scheme: TaskCreate, note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> List[TaskUpdate]:
    response = await _update_task(
        create_scheme=create_scheme,
        note_id=note_id,
        session=session
    )

    if not response:
        raise HTTPException(status_code=404, detail='The request is incorrect, check the correctness of the data')

    return response


@router.patch('/{note_id}', response_model=List[TaskUpdate])
async def partial_update_task_by_id(create_scheme: TaskCreate, note_id: uuid.UUID, session: AsyncSession = Depends(get_db)) -> List[TaskUpdate]:
    response = await _partial_update_task(
        create_scheme=create_scheme,
        note_id=note_id,
        session=session
    )

    if not response:
        raise HTTPException(status_code=404, detail='The request is incorrect, check the correctness of the data')

    return response
