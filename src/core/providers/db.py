from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import Config


class DBProvider(Provider):
    scope = Scope.APP

    @provide
    def engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(
            url=config.pg.dsn,
            echo=False,
        )

    @provide
    def pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
