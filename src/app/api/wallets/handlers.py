from dataclasses import asdict
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from app.api.wallets.schemas import LastWalletRequestsDTO, WalletInfoDTO
from logic.handlers.commands import CreateWalletRequestHandler
from logic.handlers.queries import GetLastWalletRequestsHandler

router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
)


@router.post(
    "",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Некорректный адрес"
        },
    }
)
@inject
async def wallet_info(
    address: str,
    handler: FromDishka[CreateWalletRequestHandler],
) -> WalletInfoDTO:
    try:
        return await handler.handle(address)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный адрес")


@router.get("")
@inject
async def last_requests(
    handler: FromDishka[GetLastWalletRequestsHandler],
    offset: int | None = None,
    limit: int | None = None,
) -> LastWalletRequestsDTO:
    res = await handler.handle(offset, limit)
    return LastWalletRequestsDTO.from_logic(res=res)
