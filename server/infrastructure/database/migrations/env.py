import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from server.infrastructure.database.base import Base
from server.shared.config import settings

# Import all models so Alembic can detect them for autogenerate
import server.infrastructure.orm_models.user_model  # noqa: F401
import server.infrastructure.orm_models.character_model  # noqa: F401
import server.infrastructure.orm_models.session_model  # noqa: F401
import server.infrastructure.orm_models.campaign_save_model  # noqa: F401
import server.infrastructure.orm_models.demon_model  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
