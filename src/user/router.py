from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from fastapi_users import exceptions

from .manager import get_user_manager
from .schemas import UserUpdate
from .config import current_user


verify_router = APIRouter(prefix='/verify', tags=["auth"])
reset_password_router = APIRouter(prefix='/reset', tags=["auth"])
update_router = APIRouter(prefix='/auth/update', tags=["auth"])
delete_router = APIRouter(prefix='/auth/delete', tags=["auth"])

template = Jinja2Templates(directory='tasks/auth/messages/')


@verify_router.get('/{token}/')
async def verify_email(token: str, user_manager=Depends(get_user_manager)):
    await user_manager.verify(token)

    return {
        'status': 200,
        'data': 'Почта подтверждена'
    }


@reset_password_router.get('/{token}/', response_class=HTMLResponse)
async def get_reset_password(token: str, request: Request):
    return template.TemplateResponse('reset_password.html', {'request': request, 'token': token})


@reset_password_router.post('/{token}/', status_code=201)
async def post_reset_password(token: str, user_manager=Depends(get_user_manager), password=Form(...)):
    await user_manager.reset_password(token, password)

    return {
        'data': 'Пароль обновлён'
    }


@update_router.put('/')
async def put_update_user(user_update: UserUpdate, user_manager=Depends(get_user_manager), current_user=Depends(current_user)):
    try:
        user = await user_manager.get_by_email(current_user.email)
        await user_manager.update(user_update, user)
    except exceptions.UserNotExists:
        raise HTTPException(status_code=400, detail='There is no such user')
    except exceptions.UserInactive:
        raise HTTPException(status_code=400, detail='Such user is not active')
    except exceptions.UserAlreadyVerified:
        raise HTTPException(status_code=400, detail='The user has already been verified')
    except exceptions.UserAlreadyExists:
        raise HTTPException(status_code=400, detail='Such user already exists')
    except exceptions.InvalidPasswordException:
        raise HTTPException(status_code=400, detail='The password length is at least 8 and must not contain your email')

    return None


@update_router.delete('/')
async def delete_user(user_manager=Depends(get_user_manager), current_user=Depends(current_user)):
    try:
        user = await user_manager.get_by_email(current_user.email)
        result = await user_manager.delete(user)
    except exceptions.UserNotExists:
        raise HTTPException(status_code=400, detail='There is no such user')

    return result
