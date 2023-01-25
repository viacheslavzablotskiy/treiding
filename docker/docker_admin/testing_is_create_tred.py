import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")
import django

django.setup()


class A:
    n = 5
    m = 3

    @classmethod
    def matrix(cls):
        from docker_admin.models import Trade, Offer
        offer = list(Offer.objects.filter(type_function=1))
        cls.mass(p=offer)


    @classmethod
    def mass(cls, p):
        return p





