from flask import g

LEAD_FIELDS = [
    "name",
    "expected_revenue",
    "contact_name",
    "email_from",
    "phone",
    "user_id",
    "date_deadline",
    "tag_ids",
    "description",
]


def build_leads_domain(args):
    """Build Odoo domain for listing leads from request args and context."""
    domain = []
    target_user = args.get("user_id", type=int)
    stage = args.get("stage")
    tag_id = args.get("tag_id", type=int)
    contact_id = args.get("contact_id", type=int)

    # Restrict to requester unless admin or explicit target_user provided
    if not g.is_admin:
        domain.append(("user_id", "=", g.user_id))
    elif target_user:
        domain.append(("user_id", "=", target_user))

    if stage:
        domain.append(("stage_id.name", "ilike", stage))
    if tag_id:
        domain.append(("tag_ids", "in", [tag_id]))
    if contact_id:
        domain.append(("partner_id", "=", contact_id))

    return domain


def fetch_lead(lead_id, odoo_client):
    """Read a single lead and return dict or None using given odoo client."""
    if odoo_client is None:
        raise RuntimeError("Odoo client not configured")

    result = odoo_client.execute("crm.lead", "read", [lead_id], fields=LEAD_FIELDS)
    return result[0] if result else None
