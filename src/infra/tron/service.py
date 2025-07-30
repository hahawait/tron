from dataclasses import dataclass

from tronpy import AsyncTron

from domain.entities.wallets import WalletRequest

TAddress = str


@dataclass(eq=False, frozen=True)
class TronService:
    client: AsyncTron

    async def get_wallet(
        self,
        address: TAddress,
    ) -> WalletRequest:
        if not self.client.is_address(address):
            raise ValueError("Некорректный адрес")

        account_resources = await self.client.get_account_resource(address)
        trx_balance = await self.client.get_account_balance(address)

        bandwidth = max(
            0,
            account_resources.get("freeNetLimit", 0)
            - account_resources.get("freeNetUsed", 0),
        )
        energy = max(
            0,
            account_resources.get("EnergyLimit", 0)
            - account_resources.get("EnergyUsed", 0),
        )

        return WalletRequest(
            address=address,
            trx_balance=float(trx_balance),
            bandwidth=bandwidth,
            energy=energy,
        )
