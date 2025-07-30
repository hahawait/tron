from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from logic.handlers.queries import lastWalletRequestsPaging


class WalletInfoDTO(BaseModel):
    id: UUID
    address: str
    trx_balance: float
    bandwidth: int
    energy: int
    created_at: datetime


class LastWalletRequestsDTO(BaseModel):
    total: int
    items: list[WalletInfoDTO]

    @classmethod
    def from_logic(cls, res: lastWalletRequestsPaging) -> "LastWalletRequestsDTO":
        return LastWalletRequestsDTO(
            total=res["total"],
            items=[WalletInfoDTO(**asdict(item)) for item in res["items"]],
        )
