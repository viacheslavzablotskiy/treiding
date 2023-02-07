import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")
import django

django.setup()
from datetime import datetime, timedelta
from docker_admin.models import User
from rest_framework_simplejwt.tokens import OutstandingToken
t = datetime.now()
p = list(User.objects.all())
p = p[-1]
s = OutstandingToken.objects.create(user=p, created_at=t, expires_at=timedelta(days=1))
print(s)