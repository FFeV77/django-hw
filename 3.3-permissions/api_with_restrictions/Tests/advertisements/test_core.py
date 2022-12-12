import pytest

from model_bakery import baker
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from advertisements.models import Advertisement


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_superuser('admin')


@pytest.fixture
def advert_factory():
    def factory(*args, **kwargs):
        return baker.make(Advertisement, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get(client, advert_factory):
    adverts = advert_factory(_quantity=10)

    response = client.get('/api/advertisements/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(adverts)


@pytest.mark.django_db
def test_post(client, advert_factory, user):
    client.force_authenticate(user=user)
    data = {
        "title": "Шкаф IKEA",
        "description": "Срочно",
    }

    resp1 = client.post('/api/advertisements/', data=data)
    resp2 = client.get('/api/advertisements/')

    assert resp1.status_code == 201
    assert len(resp2.json()) == 1
    assert resp2.json()[0]['title'] == data['title']


@pytest.mark.django_db
def test_patch(client, advert_factory, user):
    adverts = advert_factory(_quantity=1, creator=user)
    client.force_authenticate(user=user)
    data = {
        "title": "Шкаф IKEA",
        "description": "Срочно",
    }

    resp1 = client.get(f'/api/advertisements/{adverts[0].id}/')
    resp2 = client.patch(f'/api/advertisements/{adverts[0].id}/', data=data)
    resp3 = client.get(f'/api/advertisements/{adverts[0].id}/')

    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp3.json()['title'] == data['title']


@pytest.mark.django_db
def test_delete(client, advert_factory, user):
    adverts = advert_factory(_quantity=1, creator=user)
    client.force_authenticate(user=user)

    resp1 = client.get(f'/api/advertisements/{adverts[0].id}/')
    resp2 = client.delete(f'/api/advertisements/{adverts[0].id}/')
    resp3 = client.get(f'/api/advertisements/{adverts[0].id}/')

    assert resp1.status_code == 200
    assert resp2.status_code == 204
    assert resp3.status_code == 404


@pytest.mark.django_db
def test_add_favorite(client, advert_factory, user):
    adverts = advert_factory(_quantity=1)
    client.force_authenticate(user=user)

    resp1 = client.get(f'/api/advertisements/{adverts[0].id}/')
    resp2 = client.patch(f'/api/advertisements/{adverts[0].id}/add_favorite/')
    resp3 = client.get(f'/api/advertisements/{adverts[0].id}/')

    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp3.status_code == 200
    assert len(resp3.json()['in_favorite']) == 1


@pytest.mark.parametrize(
    ['status', 'expected_status', 'count'],
    (
        (None, 400, 10),
        ('OPEN', 400, 10),
        ('CLOSED', 201, 11),
        ('DRAFT', 201, 11),
    )
)
@pytest.mark.django_db
def test_status(client, advert_factory, user, status, expected_status, count):
    adverts = advert_factory(_quantity=10, creator=user, status='OPEN')
    client.force_authenticate(user=user)
    data = {
        "title": "Шкаф IKEA",
        "description": "Срочно",
        'status': status,
    }

    resp1 = client.post('/api/advertisements/', data=data)
    resp2 = client.get('/api/advertisements/')

    assert resp1.status_code == expected_status
    assert len(resp2.json()) == count
