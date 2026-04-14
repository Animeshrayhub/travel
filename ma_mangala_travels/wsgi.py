"""
WSGI config for Ma Mangala Travels.

On Vercel: auto-runs migrate + seed_data on cold start since /tmp is ephemeral.
Detection is path-based (/var/task) — more reliable than env vars on Vercel Lambda.
Locally: standard Django WSGI app.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ma_mangala_travels.settings')

# Detect Vercel runtime using the standard environment variable
_ON_VERCEL = os.environ.get('VERCEL') == '1'

# ── Vercel cold-start bootstrap ──────────────────────────────────────────────
# /tmp is wiped on every new Lambda instance — run migrate + seed automatically.
# The table-existence check prevents re-running on warm reuse of the same instance.
if _ON_VERCEL:
    import django
    django.setup()

    from django.core.management import call_command
    from django.db import connection

    try:
        existing_tables = connection.introspection.table_names()
    except Exception:
        existing_tables = []

    if 'travels_booking' not in existing_tables:
        try:
            call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
            call_command('seed_data', verbosity=0)
            print('[Vercel] migrate + seed_data OK', file=sys.stderr)
        except Exception as exc:
            print(f'[Vercel] Bootstrap warning: {exc}', file=sys.stderr)

# ── Standard WSGI application ────────────────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
