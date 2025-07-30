from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.wallets import WalletRequest
from infra.db.postgres.models.wallets import WalletRequestORM
from infra.db.repos.wallets import BaseWalletRequestRepo


@dataclass
class SQLAlchemyWalletRequestRepo(BaseWalletRequestRepo):
    session: AsyncSession

    async def create(self, wallet_request: WalletRequest) -> WalletRequest:
        orm = WalletRequestORM.from_entity(wallet_request)
        self.session.add(orm)
        await self.session.flush()
        return orm.to_entity()

    async def get_last_items(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[WalletRequest]:
        query = select(WalletRequestORM).order_by(WalletRequestORM.created_at.desc())
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        res = await self.session.execute(query)
        return [
            WalletRequestORM.to_entity(model) for model in res.scalars().unique().all()
        ]

    async def get_total(self) -> int:
        query = select(func.count(WalletRequestORM.id))
        res = await self.session.execute(query)
        return res.scalar_one()
