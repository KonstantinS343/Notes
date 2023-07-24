from fastapi import APIRouter, Depends

from src.user.config import current_user
from .email_verify import send_email_verify_message


router = APIRouter(prefix='/verify')


@router.get('/')
def verify_auth(user=Depends(current_user)):
    send_email_verify_message.delay(user)
    return {
        'status': 200,
        'data': 'Письмо отправлено'
    }
