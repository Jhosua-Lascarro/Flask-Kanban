FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# copy package metadata and source (README needed by build backend)
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# install runtime dependencies (no dev)
RUN uv sync --frozen --no-dev

EXPOSE 5000

CMD ["uv", "run", "--no-dev", "flask", "--app", "src.app.run:app", "run", "--host", "0.0.0.0", "--port", "5000"]
