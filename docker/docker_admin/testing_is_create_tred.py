import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")
import django

django.setup()


def matrix(a):
    s = a * 3
    if s > 1:
        return most(f=5, v=3)


def most(f, v):
    g = f + v
    return g


print(matrix(2))



