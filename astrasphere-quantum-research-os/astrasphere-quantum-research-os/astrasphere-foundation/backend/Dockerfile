# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# --- Dependency layer (cached separately from source for fast rebuilds) ---
FROM base AS deps
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install -e .

# --- Development image: live reload, dev+test deps ---
FROM deps AS development
RUN pip install -e ".[dev]"
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Production image: minimal, non-root, no dev deps ---
FROM deps AS production
RUN addgroup --system astrasphere && adduser --system --ingroup astrasphere astrasphere
COPY . .
USER astrasphere
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
