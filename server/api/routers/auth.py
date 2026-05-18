from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.schemas.auth import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from server.domain.entities.user import User
from server.infrastructure.auth.jwt_service import create_access_token, create_refresh_token
from server.infrastructure.database.base import get_db
from server.infrastructure.repositories.postgres.user_repository import PostgresUserRepository
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.auth.login_user import LoginUserUseCase
from server.use_cases.auth.refresh_token import RefreshTokenUseCase
from server.use_cases.auth.register_user import RegisterUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_repo(db: AsyncSession = Depends(get_db)) -> PostgresUserRepository:
    return PostgresUserRepository(db)


def _tokens(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    repo: PostgresUserRepository = Depends(_user_repo),
) -> TokenResponse:
    try:
        user = await RegisterUserUseCase(repo).execute(body.email, body.password, body.nickname)
        return _tokens(user)
    except InvalidActionError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    repo: PostgresUserRepository = Depends(_user_repo),
) -> TokenResponse:
    try:
        user = await LoginUserUseCase(repo).execute(body.email, body.password)
        return _tokens(user)
    except InvalidActionError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    body: RefreshRequest,
    repo: PostgresUserRepository = Depends(_user_repo),
) -> AccessTokenResponse:
    try:
        user = await RefreshTokenUseCase(repo).execute(body.refresh_token)
        return AccessTokenResponse(access_token=create_access_token(user.id))
    except (InvalidActionError, EntityNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
