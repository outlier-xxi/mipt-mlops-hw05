# syntax=docker/dockerfile:1.9

FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Build arguments
ARG MODEL_VERSION=v1.0.0

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    MODEL_VERSION=${MODEL_VERSION} \
    MODEL_PATH=/app/models/model.pkl

WORKDIR /app

# Install dependencies first (for layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy application source and install
COPY ./src /app/src
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

# Project layer
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Create models directory
RUN mkdir -p /app/models
