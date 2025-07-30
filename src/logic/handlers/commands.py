from dataclasses import dataclass

from domain.entities.wallets import WalletRequest
from infra.db.repos.wallets import BaseWalletRequestRepo
from infra.tron.service import TAddress, TronService


@dataclass(eq=False, frozen=True)
class CreateWalletRequestHandler:
    repo: BaseWalletRequestRepo
    tron: TronService

    async def handle(self, address: TAddress) -> WalletRequest:
        wallet_request: WalletRequest = await self.tron.get_wallet(address)
        return await self.repo.create(wallet_request)
