from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .manager import get_user_manager

verify_router = APIRouter(prefix='/verify', tags=["auth"])
reset_password_router = APIRouter(prefix='/reset', tags=["auth"])

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
