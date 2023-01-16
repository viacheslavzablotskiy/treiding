import pytest

from django.urls import reverse
from docker_admin.models import Currency


@pytest.mark.django_db
def test_user_create():
    Currency.objects.create(valuta="BYN")
    assert Currency.objects.count() == 1


@pytest.mark.django_db
def test_user_detail(client, django_user_model):
    user = django_user_model.objects.create(
        username='someone', password='password'
    )
    url = reverse('list_ap-detail', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 404
    assert 'someone' in response.content


