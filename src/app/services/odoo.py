from xmlrpc.client import ServerProxy

from app.config import settings


class OdooClient:
    """Simple Odoo XML-RPC client wrapper."""

    def __init__(self):
        self.common = ServerProxy(f"{settings.URL}/xmlrpc/2/common")
        self.models = ServerProxy(f"{settings.URL}/xmlrpc/2/object")
        self.uid = self.common.authenticate(
            settings.DATABASE, settings.USER, settings.API_KEY, {}
        )

    def execute(self, model, method, *args, **kwargs):
        return self.models.execute_kw(
            settings.DATABASE,
            self.uid,
            settings.API_KEY,
            model,
            method,
            args,
            kwargs,
        )


# Initialize the global Odoo client instance
try:
    odoo = OdooClient()
except Exception:
    # If initialization fails, set to None (e.g., missing credentials)
    odoo = None
