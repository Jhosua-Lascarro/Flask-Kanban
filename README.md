# Flask Kanban

REST API backend for a Kanban board powered by Odoo CRM. It authenticates users against an Odoo instance via XML-RPC, issues short-lived JWTs, and exposes CRUD endpoints for CRM leads.

- [API reference](docs/api.md)
- [Deployment](docs/deployment.md)

## Requirements

- Python ≥ 3.14
- [uv](https://github.com/astral-sh/uv)
- An Odoo instance with XML-RPC enabled and at least one API key generated

## Configuration

All settings are loaded from environment variables or a `.env` file at the project root.

| Variable | Description | Default |
| --- | --- | --- |
| `ODOO_URL` | Base URL of the Odoo instance (e.g. `https://myodoo.example`) | required |
| `ODOO_DB` | Odoo database name | required |
| `ODOO_USER` | Odoo username used for the service account; also determines who is treated as admin | required |
| `ODOO_API_KEY` | API key for the service account | required |
| `SECRET_KEY` | Secret used to sign JWTs and to validate the `X-ODOO-API-KEY` admin bypass header | required |
| `TOKEN_EXPIRE` | Token lifetime in hours | `12` |

> [!WARNING]
> `SECRET_KEY` doubles as the JWT signing secret and as the expected value of the `X-ODOO-API-KEY` header. Any request supplying that header value gains full admin access. Keep it secret and rotate it if it is ever exposed.

## Running locally

```bash
uv sync
uv run flask --app src.app.run:app run --debug
```

The server prints the listening address (for example: `Running on http://127.0.0.1:5000`).

## Running with Docker

```bash
docker build -t flask-kanban .
```

## API reference

### Authentication

**`POST /api/login`**

Request body:

```json
{ "username": "user@example.com", "api_key": "your-odoo-api-key" }
```

Returns `{ "token": "<JWT>" }` on success. The `password` field is accepted as an alias for `api_key`.

All other endpoints require one of:

- `Authorization: Bearer <token>` header
- `X-ODOO-API-KEY: <SECRET_KEY>` header — grants admin access unconditionally

 ---

### Leads

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/crm/leads` | List leads. Non-admins see only their own. | any |
| `POST` | `/api/crm/leads` | Create a lead. Non-admins are automatically set as salesperson. | any |
| `GET` | `/api/crm/leads/<id>` | Get a single lead. | any |
| `PUT` | `/api/crm/leads/<id>` | Update a lead. Non-admins can only update leads they own. | owner or admin |
| `DELETE` | `/api/crm/leads/<id>` | Delete a lead. | admin |

**Query parameters — `GET /api/crm/leads`**

| Parameter | Type | Description |
| --- | --- | --- |
| `user_id` | integer | Filter by salesperson ID. Ignored for non-admins. |
| `stage` | string | Filter by stage name (case-insensitive partial match). |
| `tag_id` | integer | Filter leads that carry this tag. |
| `contact_id` | integer | Filter by Odoo partner ID. |

---

### Tags

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/crm/tags` | List all CRM tags. | any |

---

### Users

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/crm/users` | List active internal (non-portal) users. | admin |
