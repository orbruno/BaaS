# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    PATH="/root/.local/bin:${PATH}"

# System deps commonly needed by scientific/ML and docling stack
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv (https://github.com/astral-sh/uv)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# Copy lock and project manifest first to maximize layer caching
COPY pyproject.toml uv.lock ./

# Install project dependencies into a local .venv using uv
# --frozen ensures uv.lock is respected; drop --no-dev if you want dev deps in the image
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

EXPOSE 8000

# Default command: run the API with uv+uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
