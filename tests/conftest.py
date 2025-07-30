from typing import AsyncIterable

import pytest_asyncio
import sqlalchemy as sa
from dishka import AsyncContainer, make_async_container
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.main import create_app
from core.config import get_config
from core.providers.app import AppProvider
from core.providers.db import DBProvider
from core.providers.tron import TronProvider
from core.providers.wallets import WalletProvider
from infra.db.postgres.models import BaseORM

config = get_config()

DB_URL = config.pg.dsn.replace(f"/{config.pg.db}", "")
TEST_DB_NAME = config.pg.db
TEST_DB_URL = config.pg.dsn

@pytest_asyncio.fixture
def test_address() -> str:
    return "TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7"


@pytest_asyncio.fixture
async def test_database() -> AsyncIterable[None]:
    admin_engine = create_async_engine(DB_URL, isolation_level="AUTOCOMMIT")
    async with admin_engine.begin() as conn:
        await conn.execute(sa.text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        await conn.execute(sa.text(f"CREATE DATABASE {TEST_DB_NAME}"))

    test_engine = create_async_engine(TEST_DB_URL)
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    async with admin_engine.begin() as conn:
        # Закрыть все соединения перед удалением БД
        await conn.execute(
            sa.text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
        )
        await conn.execute(sa.text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
    await admin_engine.dispose()
    await test_engine.dispose()


@pytest_asyncio.fixture
async def container() -> AsyncIterable[AsyncContainer]:
    container = make_async_container(
        AppProvider(),
        DBProvider(),
        TronProvider(),
        WalletProvider(),
    )
    yield container
    await container.close()


@pytest_asyncio.fixture
async def async_client(
    test_database: None,
) -> AsyncIterable[AsyncClient]:
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
