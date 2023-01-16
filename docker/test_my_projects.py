import pytest

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_view(client):
    url = reverse('list_ap-list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_views(client):
    url = reverse('item-list')
    response = client.get(url)
    assert response.status_code == 200
