from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass(eq=False, kw_only=True)
class WalletRequest(BaseEntity):
    address: str
    trx_balance: float
    bandwidth: int
    energy: int
