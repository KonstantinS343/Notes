from fastapi import APIRouter, Depends

from .manager import get_user_manager

router = APIRouter(prefix='/verify', tags=["auth"])


@router.get('/{token}/')
async def verify_email(token: str, user_manager=Depends(get_user_manager)):
    await user_manager.verify(token)

    return {
        'status': 200,
        'data': 'Почта подтверждена'
    }
