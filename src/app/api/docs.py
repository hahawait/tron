from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from starlette.responses import HTMLResponse, JSONResponse

http_basic = HTTPBasic(auto_error=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def secure_docs(
    app: FastAPI,
    *,
    admin_username: str,
    admin_password: str,
    title: str,
    version: str = "0.2.0",
    description: str | None = None,
    docs_url: str = "/api/docs",
    openapi_url: str = "/api/openapi.json",
    **kwargs,  # noqa: ANN003
) -> None:
    admin_username = pwd_context.hash(admin_username)
    admin_password = pwd_context.hash(admin_password)

    def get_admin_user(
        credentials: HTTPBasicCredentials = Depends(http_basic),
    ) -> None:
        if pwd_context.verify(
            credentials.username, admin_username
        ) and pwd_context.verify(credentials.password, admin_password):
            return
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )

    @app.get(
        openapi_url, include_in_schema=False, dependencies=[Depends(get_admin_user)]
    )
    async def get_open_api_endpoint() -> JSONResponse:
        return JSONResponse(
            get_openapi(
                title=title, version=version, description=description, routes=app.routes
            )
        )

    @app.get(docs_url, include_in_schema=False, dependencies=[Depends(get_admin_user)])
    async def get_documentation() -> HTMLResponse:
        return get_swagger_ui_html(openapi_url=openapi_url, title=title)
