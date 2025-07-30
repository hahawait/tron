from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api.docs import secure_docs
from app.api.middlewares import build_middlewares
from app.api.wallets.handlers import router as wallet_router
from app.logger.logger import init_logger
from core.config import get_config
from core.providers.app import AppProvider
from core.providers.db import DBProvider
from core.providers.tron import TronProvider
from core.providers.wallets import WalletProvider


def create_app() -> FastAPI:
    config = get_config()
    init_logger(config.app.log_level)

    fastapi_params = dict(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        middleware=build_middlewares(),
    )

    if config.app.is_prod:
        app = FastAPI(
            **fastapi_params,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            debug=True,
        )
        secure_docs(
            app=app,
            admin_username=config.app.admin_username,
            admin_password=config.app.admin_password,
            **fastapi_params,
        )
    else:
        app = FastAPI(**fastapi_params, debug=True)

    container = make_async_container(
        AppProvider(),
        DBProvider(),
        TronProvider(),
        WalletProvider(),
    )
    setup_dishka(container, app)

    app.include_router(wallet_router)

    return app
