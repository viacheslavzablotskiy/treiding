import os

from django.db.models import Min

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")

import django

django.setup()

from django.core.management import call_command

from docker_admin.models import Offer, Trade

l = [0, 2, 5, 6, 7]
for i in l:
        p = 5
        if p in l:
                s = l.index(p)
                p = 3

        print(i)
        





