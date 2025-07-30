FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /project

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY src src
# COPY tests tests
COPY pyproject.toml uv.lock ./
COPY alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV PATH="/project/.venv/bin:$PATH"
ENV PYTHONPATH="/project/src"
