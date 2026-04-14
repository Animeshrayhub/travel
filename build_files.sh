#!/bin/bash
# Vercel build script — runs during deployment build phase

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Build complete ==="
