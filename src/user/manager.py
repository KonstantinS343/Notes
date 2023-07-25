import uuid
from typing import Union, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException

from src.user.models import User
from src.user.utils import get_user_db
from src.settings import SECRET
from src.user.schemas import UserCreate
from tasks.auth.email_verify import send_email_verify_message


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        send_email_verify_message.delay(user.email)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        await self.verify(token=token, request=request)

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
