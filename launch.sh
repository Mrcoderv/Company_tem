#!/usr/bin/env bash
# =============================================================================
# launch.sh — one-command launcher for the merged Pivot Risk Django project.
#
# What it does on every run:
#   1. Creates a Python venv in backend/.venv if missing (and installs deps).
#   2. Applies any pending database migrations.
#   3. Creates the "admin" superuser on first run (if none exists).
#   4. Starts the Django dev server.
#
# Overridable env vars:
#   HOST             bind address            (default: 127.0.0.1)
#   PORT             port                    (default: 8000)
#   DJANGO_SUPERUSER_PASSWORD   superuser password (default: PivotRisk@2026)
#
# Example:
#   ./launch.sh                       # http://127.0.0.1:8000
#   PORT=9000 ./launch.sh             # http://127.0.0.1:9000
# =============================================================================

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$ROOT"

# 1) Virtualenv + dependencies ----------------------------------------------
if [ ! -d ".venv" ]; then
  echo "==> Creating virtual environment (.venv) ..."
  "$PYTHON_BIN" -m venv .venv
fi

PY="$BACKEND/.venv/bin/python"

if ! "$PY" -c "import django" >/dev/null 2>&1; then
  echo "==> Installing dependencies ..."
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet \
    "Django==5.2.7" \
    "Pillow==11.3.0" \
    "asgiref==3.9.2" \
    "sqlparse==0.5.3" \
    "tzdata==2025.2"
fi

# 2) Migrations ---------------------------------------------------------------
echo "==> Applying database migrations ..."
"$PY" manage.py migrate --noinput

# 3) Superuser (first run only) -------------------------------------------------
SUPERUSERS="$(
  "$PY" manage.py shell -c \
    "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(is_superuser=True).exists())" \
    2>/dev/null | tail -1
)"
if [ "$SUPERUSERS" != "True" ]; then
  echo "==> No superuser found — creating 'admin' (password: ${DJANGO_SUPERUSER_PASSWORD:-PivotRisk@2026}) ..."
  DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-PivotRisk@2026}" \
    "$PY" manage.py createsuperuser \
    --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
    --email "${DJANGO_SUPERUSER_EMAIL:-admin@pivotrisk.com.np}" \
    --noinput
fi

# 4) Run --------------------------------------------------------------------------
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
echo ""
echo "==> Site   : http://$HOST:$PORT"
echo "==> Admin  : http://$HOST:$PORT/admin/"
echo "==> Press Ctrl+C to stop."
echo ""
exec "$PY" manage.py runserver "$HOST:$PORT"
