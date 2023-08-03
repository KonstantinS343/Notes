import uuid
from typing import Union, Optional, Any, Coroutine

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException, schemas, exceptions

from src.user.models import User
from src.user.utils import get_user_db
from src.settings import SECRET
from src.user.schemas import UserCreate
from tasks.auth.email_verify import send_email_verify_message
from tasks.auth.reset_password import send_email_reset_password_message
from tasks.auth.delete_notification import send_email_delete_notification
from src.user.utils import _get_user_by_username


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

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_email_verify_message.delay(user.email, token)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        await self.request_verify(user, request)

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")

    async def create(self, user_create: schemas.UC, safe: bool = False, request: Request | None = None) -> Coroutine[Any, Any, User]:
        response = await _get_user_by_username(user_create.username)

        if response:
            raise exceptions.UserAlreadyExists()
        else:
            return await super().create(user_create, safe, request)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_email_reset_password_message.delay(user.email, token)

    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        send_email_delete_notification.delay(user.email)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
