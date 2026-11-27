"""Alembic runner: applies migration files to the database named by our app Settings."""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from store.config import get_settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)  # logging setup from alembic.ini

# Same DB address as the app (DB_HOST, DB_PASSWORD, ...): one source of truth, no URL in .ini
database_url = get_settings().database_url

target_metadata = None  # step 4: our table models' metadata, so Alembic can autogenerate changes


def run_migrations_offline() -> None:
    """`alembic upgrade head --sql`: print the SQL instead of running it (for review)."""
    context.configure(url=database_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():  # each run is one transaction: all-or-nothing
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_async_engine(database_url, poolclass=pool.NullPool)  # one-off: no pool
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)  # Alembic itself is sync code
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
