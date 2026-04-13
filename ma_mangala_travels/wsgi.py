"""
WSGI config for Ma Mangala Travels.

On Vercel: auto-runs migrate + seed_data on cold start since /tmp is ephemeral.
Locally: standard Django WSGI app.
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ma_mangala_travels.settings')

# ── Vercel cold-start bootstrap ──────────────────────────────────────────────
# /tmp is wiped between deployments on Vercel, so we must migrate + seed each
# time a new Lambda instance spins up. This adds ~1s to the first request only.
if os.environ.get('VERCEL'):
    import django
    django.setup()

    from django.core.management import call_command
    from django.db import connection

    # Check if tables already exist (avoid re-running on warm instances)
    try:
        existing_tables = connection.introspection.table_names()
    except Exception:
        existing_tables = []

    if 'travels_booking' not in existing_tables:
        # Fresh /tmp — run migrations and seed default data
        try:
            call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
            call_command('seed_data', verbosity=0)
            print("[Vercel Bootstrap] Migrations + seed_data completed.", file=sys.stderr)
        except Exception as e:
            print(f"[Vercel Bootstrap] Warning: {e}", file=sys.stderr)

# ── Standard WSGI application ────────────────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
