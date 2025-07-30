from __future__ import annotations

from sqlalchemy import FLOAT, INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.wallets import WalletRequest
from infra.db.postgres.models.base import BaseORM


class WalletRequestORM(BaseORM):
    __tablename__ = "wallet_requests"

    address: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    trx_balance: Mapped[float] = mapped_column(FLOAT, nullable=False)
    bandwidth: Mapped[int] = mapped_column(INTEGER, nullable=False)
    energy: Mapped[int] = mapped_column(INTEGER, nullable=False)

    def __repr__(self) -> str:
        return f"<WalletRequestORM id={self.id} address={self.address}>"

    def __str__(self) -> str:
        return f"WalletRequestORM(id={self.id}, address={self.address})"

    @staticmethod
    def from_entity(entity: WalletRequest) -> "WalletRequestORM":
        return WalletRequestORM(
            id=entity.id,
            address=entity.address,
            trx_balance=entity.trx_balance,
            bandwidth=entity.bandwidth,
            energy=entity.energy,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> WalletRequest:
        return WalletRequest(
            id=self.id,
            address=self.address,
            trx_balance=self.trx_balance,
            bandwidth=self.bandwidth,
            energy=self.energy,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
