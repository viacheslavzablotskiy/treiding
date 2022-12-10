from django.contrib.auth.base_user import BaseUserManager
from rest_framework.response import Response
from .serializers import *

from .models import *


class UserManager(BaseUserManager):
    pass

