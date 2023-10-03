from logging import getLogger

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.user import (
    _get_user_by_id,
    _update_user,
)
from api.handlers.user import user_router
from db.models import User
from db.session import get_async_session

from api.schemas.user import UpdatedUserResponse

logger = getLogger(__name__)


@user_router.patch("/admin_privilege", response_model=UpdatedUserResponse)
async def grant_admin_privilege(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail='Forbidden.')
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400,
            detail='Cannot manage privileges of itself.',
        )
    user_for_promotion = await _get_user_by_id(user_id, session)
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f'User with id {user_id} '
                   f'already promoted to admin / superadmin.',
        )
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404,
            detail=f'User with id:{user_id} not found'
        )
    updated_user_params = {
        "roles": user_for_promotion.enrich_admin_roles_by_admin_role()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params,
            session=session,
            user_id=user_id,
        )
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=503, detail=f'DB ERROR: {e}')
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/admin_privilege", response_model=UpdatedUserResponse)
async def revoke_admin_privilege(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail='Forbidden.')
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400,
            detail='Cannot manage privileges of itself.',
        )
    user_for_revoke_admin_privileges = await _get_user_by_id(user_id, session)
    if not user_for_revoke_admin_privileges.is_admin:
        raise HTTPException(
            status_code=409,
            detail=f'User with id {user_id} has no admin privileges.',
        )
    if user_for_revoke_admin_privileges is None:
        raise HTTPException(
            status_code=404,
            detail=f'User with id:{user_id} not found',
        )
    updated_user_params = {
        'roles': user_for_revoke_admin_privileges
        .remove_admin_privileges_from_model()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params,
            session=session,
            user_id=user_id,
        )
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=503, detail=f'DB ERROR: {e}')
    return UpdatedUserResponse(updated_user_id=updated_user_id)
