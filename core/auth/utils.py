from datetime import datetime
from typing import Optional
from fastapi import Security, HTTPException
from jose import jwt
from jose.exceptions import JWTError
from starlette.status import HTTP_403_FORBIDDEN

from core.auth.schemas import JWTTokenPayload
from apps.user.models import UserInfo
from fastapi.security import OAuth2AuthorizationCodeBearer
from settings.config import settings


async def authenticate(address) -> Optional[UserInfo]:
    if address:
        user = await UserInfo.get_or_none(address=address)
    else:
        return None

    if user is None:
        return None

    # code_obj = await InviteCodePool.filter(used_user__address=address).first()
    # if not code_obj or not code_obj.is_used:
    #     return None

    return user


async def update_last_login(user_id: int) -> None:
    user = await UserInfo.get(id=user_id)
    user.last_login = datetime.now()
    await user.save()


reusable_oauth2 = OAuth2AuthorizationCodeBearer(
    tokenUrl="/api/auth/access-token",
    authorizationUrl="/api/auth/access-token",
    refreshUrl="/api/auth/refresh-access-token",
)

reusable_oauth2_optional = OAuth2AuthorizationCodeBearer(
    tokenUrl="/api/auth/access-token",
    authorizationUrl="/api/auth/access-token",
    refreshUrl="/api/auth/refresh-access-token",
    auto_error=False
)


async def get_current_user(token: str = Security(reusable_oauth2)) -> Optional[UserInfo]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await UserInfo.filter(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User not found")
    return user


async def get_current_user_optional(token: str = Security(reusable_oauth2_optional)) -> Optional[UserInfo]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except JWTError:
        return None
    user = await UserInfo.filter(id=token_data.user_id)
    return user
