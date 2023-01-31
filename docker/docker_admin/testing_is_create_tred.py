import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")
import django

django.setup()


def matrix(a, b):
    s = a + b
    most(v=a, f=b)
    return most(f=a, v=b)


def most(f, v):
    g = f + v
    return g


print(matrix(2, 3))
