import logging
from apps.user.models import UserInfo
from core.utils.base_util import get_limiter
from fastapi import APIRouter
from starlette.requests import Request
from core.utils.tool_util import success, error

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/user")


@router.get('', tags=['user'])
@limiter.limit('100/minute')
async def user_info(request: Request, address: str):
    user = await UserInfo.filter(address=address.lower()).first()
    if not user:
        return error('not find')
    return success(user)
