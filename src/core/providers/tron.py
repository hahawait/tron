from dishka import Provider, Scope, provide
from tronpy import AsyncTron

from core.config import Config
from infra.tron.service import TronService


class TronProvider(Provider):
    scope = Scope.APP

    @provide
    def client(self, config: Config) -> AsyncTron:
        return AsyncTron(network=config.tron.network)

    @provide(scope=Scope.REQUEST)
    def tron_service(self, client: AsyncTron) -> TronService:
        return TronService(client)
        # async with client:
        #     yield TronService(client)
