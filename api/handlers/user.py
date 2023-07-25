from logging import getLogger

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.permission import check_user_permissions
from api.actions.user import (
    _create_new_user,
    _get_user_by_id,
    _delete_user,
    _update_user,
)
from db.models import User
from db.session import get_async_session

from api.schemas.user import (
    UserCreate,
    ShowUser,
    DeleteUserResponse,
    UpdatedUserRequest,
    UpdatedUserResponse,
)

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post('/', response_model=ShowUser)
async def create_user(
        body: UserCreate,
        session: AsyncSession = Depends(get_async_session)
) -> ShowUser:
    try:
        return await _create_new_user(body, session)
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=503, detail=f'DB ERROR: {e}')


@user_router.get('/', response_model=ShowUser)
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with id:{user_id} not found'
        )
    return user


@user_router.patch('/', response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: int,
        body: UpdatedUserRequest,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail='Empty request body, provide at least one parameter'
        )
    user_for_update = await _get_user_by_id(user_id, session)
    if not user_for_update:
        raise HTTPException(
            status_code=404,
            detail=f'User with id:{user_id} not found'
        )
    if user_id != current_user.user_id and check_user_permissions(
            target_user=user_for_update,
            current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail='Forbidden.')
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


@user_router.delete('/', response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, session)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404,
            detail=f'User with id {user_id} not found.',
        )
    if not check_user_permissions(
            target_user=user_for_deletion,
            current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    delete_user_id = await _delete_user(user_id, session)
    if not delete_user_id:
        raise HTTPException(
            status_code=404,
            detail=f'User with id:{user_id} not found'
        )
    return DeleteUserResponse(delete_user_id=delete_user_id)
