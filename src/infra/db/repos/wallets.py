from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.wallets import WalletRequest


@dataclass
class BaseWalletRequestRepo(ABC):
    @abstractmethod
    async def create(self, wallet_request: WalletRequest) -> WalletRequest:
        raise NotImplementedError

    @abstractmethod
    async def get_last_items(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[WalletRequest]:
        raise NotImplementedError

    @abstractmethod
    async def get_total(self) -> int:
        raise NotImplementedError
