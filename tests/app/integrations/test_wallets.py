import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_wallet_info(
    async_client: AsyncClient,
    test_address: str,
) -> None:
    # ОК
    response = await async_client.post(
        url="/wallets",
        params={
            "address": test_address
        },
    )
    assert response.status_code == 200

    # Некорректный адрес
    response = await async_client.post(
        url="/wallets",
        params={
            "address": "incorrect_address"
        },
    )
    assert response.status_code == 400   


@pytest.mark.asyncio
async def test_last_requests(
    async_client: AsyncClient,
    test_address: str,
) -> None:
    # Setup
    for i in range(5):
        response = await async_client.post(
            url="/wallets",
            params={
                "address": test_address
            },
        )
        assert response.status_code == 200

    # Без фильтров 
    response = await async_client.get(
        url="/wallets",
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 5

    # Пагинация
    response = await async_client.get(
        url="/wallets",
        params={
            "offset": 1,
            "limit": 3,
        }
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3
