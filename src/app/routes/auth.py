from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from jwt import encode

import app.services.odoo as odoo_module
from app.config import settings

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user with Odoo API key and return JWT"""
    data = request.json or {}

    # Authenticate using API key instead of password
    if not odoo_module.odoo or odoo_module.odoo.common is None:
        return jsonify({"error": "Odoo client not configured"}), 500

    # Get username and api_key from request
    username = data.get("username")
    api_key = data.get("api_key") or data.get("password")  # Support both field names

    if not username or not api_key:
        return jsonify({"error": "Missing username or api_key"}), 400

    try:
        # Try to authenticate using the API key
        uid = odoo_module.odoo.common.authenticate(
            settings.DATABASE, username, api_key, {}
        )
    except Exception as e:
        return jsonify({"error": f"Authentication failed: {str(e)}"}), 401

    if uid:
        # Mark admin by configured username and issue token
        is_admin = username == settings.USER
        token = encode(
            {
                "user_id": uid,
                "is_admin": is_admin,
                "exp": datetime.now(timezone.utc) + timedelta(hours=settings.EXPIRE),
            },
            settings.SECRET_KEY,
        )
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
