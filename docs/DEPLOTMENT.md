# Deployment

## Prerequisites

- [uv](https://github.com/astral-sh/uv) ≥ 0.10.2
- Python ≥ 3.14 (managed automatically by uv)
- A running Odoo instance with XML-RPC enabled

## Environment file

Create a `.env` file at the project root before running anything:

```env
ODOO_URL=https://myodoo.example.com
ODOO_DB=mydb
ODOO_USER=admin@example.com
ODOO_API_KEY=your-odoo-api-key
SECRET_KEY=change-me-to-a-long-random-string
TOKEN_EXPIRE=12
```

> [!CAUTION]
> Never commit `.env` to version control. It contains the `SECRET_KEY` which signs all JWTs and grants admin bypass access if leaked.

---

## Local development

```bash
uv sync
uv run flask --app src.app.run:app run --debug
```

The app listens on `http://127.0.0.1:5000` by default.

> [!NOTE]
> `uv sync` installs both runtime and dev dependencies. Use `uv sync --no-dev` to replicate the production install.

---

## Docker

### Build

```bash
docker build -t flask-kanban .
```

### Run

```bash
docker run --env-file .env -p 5000:5000 flask-kanban
```

The container exposes port `5000`. Map it to any host port with `-p <host>:5000`.

### Environment variables at runtime

Avoid baking secrets into the image. Pass all variables at runtime via `--env-file` or individual `-e` flags:

```bash
docker run \
  -e ODOO_URL=https://myodoo.example.com \
  -e ODOO_DB=mydb \
  -e ODOO_USER=admin@example.com \
  -e ODOO_API_KEY=... \
  -e SECRET_KEY=... \
  -p 5000:5000 \
  flask-kanban
```

> [!WARNING]
> Do not use `ENV` instructions in the `Dockerfile` for secrets. They are visible in `docker inspect` and in image layers.
