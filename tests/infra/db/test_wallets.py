import pytest
from dishka import AsyncContainer

from domain.entities.wallets import WalletRequest
from infra.db.repos.wallets import BaseWalletRequestRepo


@pytest.mark.asyncio
async def test_wallet_info(
    test_database: None,
    container: AsyncContainer,
    test_address: str,
) -> None:
    async with container() as request_container:
        repo = await request_container.get(BaseWalletRequestRepo)
        wallet_request: WalletRequest = WalletRequest(
            address=test_address,
            trx_balance=1000.0,
            bandwidth=10,
            energy=10
        )
        res = await repo.create(wallet_request)

        assert res.address == wallet_request.address
        assert res.trx_balance == wallet_request.trx_balance
        assert res.bandwidth == wallet_request.bandwidth
        assert res.id == wallet_request.id
