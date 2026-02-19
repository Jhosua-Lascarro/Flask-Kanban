from functools import wraps

from flask import g, jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError, decode

from app.config import settings


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Admin bypass using Odoo API key header
        api_key_header = request.headers.get("X-ODOO-API-KEY")
        if api_key_header == settings.SECRET_KEY:
            g.user_id = settings.USER
            g.is_admin = True
            return f(*args, **kwargs)

        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "No authentication method provided"}), 401

        try:
            # Decode JWT and set identity and admin flag
            data = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            g.user_id = data["user_id"]
            g.is_admin = data.get("is_admin", False)
        except InvalidTokenError, ExpiredSignatureError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated
