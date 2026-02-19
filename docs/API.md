# API Reference

Base URL: `http://<host>:5000/api`

All protected endpoints require one of the following headers:

| Header | Value | Notes |
| --- | --- | --- |
| `Authorization` | `Bearer <token>` | JWT obtained from `/api/login` |
| `X-ODOO-API-KEY` | `<SECRET_KEY>` | Grants unconditional admin access |

> [!WARNING]
> `X-ODOO-API-KEY` bypasses all user-level checks. It should only be used for internal service-to-service calls, never from a browser client.

 ---

## Authentication

### `POST /api/login`

Authenticates against Odoo and returns a signed JWT.

#### **Request**

```json
{
  "username": "user@example.com",
  "api_key": "your-odoo-api-key"
}
```

`password` is accepted as an alias for `api_key`.

**Response `200`**

```json
{
  "token": "<JWT>"
}
```

**Response `400`** — missing `username` or `api_key`

```json
{ "error": "Missing username or api_key" }
```

**Response `401`** — wrong credentials

```json
{ "error": "Invalid credentials" }
```

The JWT payload contains `user_id`, `is_admin`, and `exp`. Tokens expire after `TOKEN_EXPIRE` hours (default: 12).

 ---

## Leads

### `GET /api/crm/leads`

Returns a list of leads. Non-admins receive only leads assigned to them.

#### **Query parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `user_id` | integer | Filter by salesperson ID. Admins only; ignored for non-admins. |
| `stage` | string | Filter by stage name (case-insensitive partial match). |
| `tag_id` | integer | Filter leads that carry this tag. |
| `contact_id` | integer | Filter by Odoo partner ID. |

**Response `200`**

```json
[
  {
    "name": "Acme deal",
    "expected_revenue": 5000.0,
    "contact_name": "John Doe",
    "email_from": "john@acme.com",
    "phone": "+1 555 0100",
    "user_id": [3, "Alice"],
    "date_deadline": "2026-03-01",
    "tag_ids": [1, 4],
    "description": "..."
  }
]
```

 ---

### `POST /api/crm/leads`

Creates a lead. Non-admins are automatically set as the salesperson regardless of what `user_id` is sent.

#### **Request body**

```json
{
  "name": "New opportunity",
  "expected_revenue": 1200.0,
  "contact_name": "Jane Smith",
  "email_from": "jane@example.com"
}
```

Any field accepted by the Odoo `crm.lead` model can be included.

**Response `201`**

```json
{ "id": 42 }
```

 ---

### `GET /api/crm/leads/<id>`

Returns a single lead by its Odoo record ID.

**Response `200`** — same structure as a single item from `GET /api/crm/leads`

**Response `404`**

```json
{ "error": "Lead not found" }
```

 ---

### `PUT /api/crm/leads/<id>`

Updates a lead. Non-admins can only update leads assigned to them.

#### **Request** — any subset of `crm.lead` fields

```json
{
  "expected_revenue": 8000.0,
  "date_deadline": "2026-04-15"
}
```

**Response `200`**

```json
{ "status": "updated" }
```

**Response `403`** — non-admin attempting to update another user's lead

```json
{ "error": "Unauthorized" }
```

 ---

### `DELETE /api/crm/leads/<id>`

Deletes a lead. Admin only.

**Response `200`**

```json
{ "status": "deleted" }
```

**Response `403`**

```json
{ "error": "Only administrators can delete" }
```

 ---

## Tags

### `GET /api/crm/tags`

Returns all CRM tags.

**Response `200`**

```json
[
  { "id": 1, "name": "Hot" },
  { "id": 2, "name": "Renewal" }
]
```

 ---

## Users

### `GET /api/crm/users`

Returns active internal (non-portal) users. Admin only.

**Response `200`**

```json
[
  { "id": 3, "name": "Alice", "login": "alice@example.com", "email": "alice@example.com" }
]
```

**Response `403`**

```json
{ "error": "Restricted to administrators" }
```
