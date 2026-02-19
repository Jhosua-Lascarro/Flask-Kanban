from flask import Blueprint, g, jsonify, request

import app.services.odoo as odoo_module
from app.utils.auth import require_auth
from app.utils.helpers import LEAD_FIELDS, build_leads_domain, fetch_lead

crm_bp = Blueprint("crm", __name__)


TAG_FIELDS = ["id", "name"]
USER_FIELDS = ["id", "name", "login", "email"]


# Endpoints
@crm_bp.route("/leads", methods=["GET"])
@require_auth
def get_leads():
    """List leads with optional filters."""
    domain = build_leads_domain(request.args)
    if odoo_module.odoo is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    leads = odoo_module.odoo.execute(
        "crm.lead", "search_read", domain, fields=LEAD_FIELDS
    )
    return jsonify(leads), 200


@crm_bp.route("/leads", methods=["POST"])
@require_auth
def create_lead():
    """Create a lead; non-admins are set as salesperson."""
    data = request.json or {}
    if not g.is_admin:
        data["user_id"] = g.user_id

    if odoo_module.odoo is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    new_id = odoo_module.odoo.execute("crm.lead", "create", data)
    return jsonify({"id": new_id}), 201


@crm_bp.route("/leads/<int:lead_id>", methods=["GET"])
@require_auth
def get_lead_detail(lead_id):
    """Return a single lead or 404."""
    try:
        lead = fetch_lead(lead_id, odoo_module.odoo)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404
        return jsonify(lead), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crm_bp.route("/leads/<int:lead_id>", methods=["PUT"])
@require_auth
def update_lead(lead_id):
    """Update a lead: only owner or admin allowed."""
    lead = fetch_lead(lead_id, odoo_module.odoo)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    # owner is a tuple/list like [id, name]
    owner = lead.get("user_id")
    owner_id = owner[0] if owner else None
    if not g.is_admin and owner_id != g.user_id:
        return jsonify({"error": "Unauthorized"}), 403
    if odoo_module.odoo is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    odoo_module.odoo.execute("crm.lead", "write", [lead_id], request.json or {})
    return jsonify({"status": "updated"}), 200


@crm_bp.route("/leads/<int:lead_id>", methods=["DELETE"])
@require_auth
def delete_lead(lead_id):
    """Delete a lead (admin only)."""
    if not g.is_admin:
        return jsonify({"error": "Only administrators can delete"}), 403
    if odoo_module.odoo is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    odoo_module.odoo.execute("crm.lead", "unlink", [lead_id])
    return jsonify({"status": "deleted"}), 200


@crm_bp.route("/tags", methods=["GET"])
@require_auth
def get_tags():
    """List CRM tags."""
    if odoo_module.odoo is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    tags = odoo_module.odoo.execute("crm.tag", "search_read", [], fields=TAG_FIELDS)
    return jsonify(tags), 200


@crm_bp.route("/users", methods=["GET"])
@require_auth
def get_users():
    """Admin-only: list internal active users."""
    if not g.is_admin:
        return jsonify({"error": "Restricted to administrators"}), 403

    try:
        if odoo_module.odoo is None:
            return ("Odoo client not configured", 500)

        domain = [("share", "=", False), ("active", "=", True)]
        users = odoo_module.odoo.execute(
            "res.users", "search_read", domain, fields=USER_FIELDS
        )
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
