from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.postgres.repos.wallets.sqlalchemy import SQLAlchemyWalletRequestRepo
from infra.db.repos.wallets import BaseWalletRequestRepo
from infra.tron.service import TronService
from logic.handlers.commands import CreateWalletRequestHandler
from logic.handlers.queries import GetLastWalletRequestsHandler


class WalletProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def wallet_repo(self, session: AsyncSession) -> BaseWalletRequestRepo:
        return SQLAlchemyWalletRequestRepo(session)

    @provide
    async def create_wallet(
        self,
        repo: BaseWalletRequestRepo,
        tron_service: TronService,
    ) -> CreateWalletRequestHandler:
        return CreateWalletRequestHandler(
            repo=repo,
            tron=tron_service,
        )

    @provide
    async def get_last_wallet_requests(
        self,
        repo: BaseWalletRequestRepo,
    ) -> GetLastWalletRequestsHandler:
        return GetLastWalletRequestsHandler(repo)
