import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_intro.settings")

from django.core.management import call_command
from django.db import OperationalError
from company_intro.wsgi import application

# A fresh Vercel instance has an empty writable /tmp filesystem. Apply the
# bundled migrations once so the editable site can render on a cold start.
try:
    call_command("migrate", interactive=False, verbosity=0)
except OperationalError:
    # Keep Django's normal error handling if the database is temporarily
    # unavailable; the request should still be served by the WSGI app.
    pass

app = application
