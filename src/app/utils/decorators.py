from functools import wraps

from flask import g, jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError, decode

from app.config import settings


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Expect: Authorization: Bearer <token>
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            # Decode JWT and attach minimal identity to request context
            data = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            g.user_id = data["user_id"]
            g.user_login = data.get("login")
        except ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
