# Ambiente Linux reprodutível para testes, treino e CI.
# NÃO serve para a câmara nem para o Arduino (ver README).
FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Bibliotecas de sistema que o OpenCV/MediaPipe precisam em Linux
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# venv fora de /app: o .venv do host (Windows/macOS) não funciona dentro de Linux
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock* .python-version ./
RUN uv sync --group dev --no-install-project

COPY . .
CMD ["uv", "run", "pytest"]
