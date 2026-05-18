from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from server.domain.entities.user import User
from server.domain.ports.user_repository import UserRepository
from server.infrastructure.auth.jwt_service import decode_access_token
from server.infrastructure.repositories.postgres.user_repository import PostgresUserRepository
from server.infrastructure.database.base import get_db
from server.shared.exceptions import InvalidActionError
from sqlalchemy.ext.asyncio import AsyncSession

_bearer = HTTPBearer()


def _user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return PostgresUserRepository(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    repo: UserRepository = Depends(_user_repo),
) -> User:
    try:
        user_id = decode_access_token(credentials.credentials)
    except InvalidActionError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
