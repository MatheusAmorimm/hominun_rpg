from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.entities.user import User
from server.domain.ports.user_repository import UserRepository
from server.infrastructure.orm_models.user_model import UserModel


def _to_domain(row: UserModel) -> User:
    return User(
        id=row.id,
        email=row.email,
        password_hash=row.password_hash,
        nickname=row.nickname,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        existing = await self._session.get(UserModel, user.id)
        if existing:
            existing.email = user.email
            existing.password_hash = user.password_hash
            existing.nickname = user.nickname
        else:
            self._session.add(UserModel(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash,
                nickname=user.nickname,
            ))

    async def get_by_id(self, user_id: UUID) -> User | None:
        row = await self._session.get(UserModel, user_id)
        return _to_domain(row) if row else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None
