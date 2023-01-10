import os

from django.db.models import Min

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")

import django

django.setup()

from django.core.management import call_command







