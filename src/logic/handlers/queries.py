from dataclasses import dataclass

from domain.entities.wallets import WalletRequest
from infra.db.repos.wallets import BaseWalletRequestRepo

lastWalletRequestsPaging = dict[str, int | list[WalletRequest]]

@dataclass(eq=False, frozen=True)
class GetLastWalletRequestsHandler:
    repo: BaseWalletRequestRepo

    async def handle(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ) -> lastWalletRequestsPaging:
        last_items: list[WalletRequest] = await self.repo.get_last_items(
            offset=offset,
            limit=limit,
        )
        total: int = await self.repo.get_total()
        return {
            "total": total,
            "items": last_items,
        }
