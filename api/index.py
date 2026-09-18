import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_intro.settings")

from company_intro.wsgi import application

app = application
