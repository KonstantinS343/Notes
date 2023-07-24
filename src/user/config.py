from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users import FastAPIUsers

import uuid

from src.settings import SECRET
from .models import User
from .manager import get_user_manager


cookie_transport = CookieTransport(cookie_name='note', cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
