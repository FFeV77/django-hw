import pytest

from model_bakery import baker
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from advertisements.models import Advertisement


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def users():
    return {
        'anon': None,
        'admin': User.objects.create_superuser('admin'),
        'user1': User.objects.create_user('test1'),
        'user2': User.objects.create_user('test2'),
    }


@pytest.fixture
def advert_factory():
    def factory(*args, **kwargs):
        return baker.make(Advertisement, *args, **kwargs)
    return factory


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['tested_user', 'expected_status'],
    (
        ('anon', 401),
        ('admin', 201),
        ('user1', 201),
        ('user2', 201),
    )
)
def test_creation(client, users, tested_user, expected_status):
    client.force_authenticate(user=users[tested_user])
    data = {
        "title": "Шкаф IKEA",
        "description": "Срочно"
    }

    response = client.post('/api/advertisements/', data=data)

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['tested_user', 'expected_status'],
    (
        ('anon', 401),
        ('admin', 200),
        ('user1', 200),
        ('user2', 403),
    )
)
def test_patch(client, advert_factory, users, tested_user, expected_status):
    adverts = advert_factory(_quantity=1, creator=users['user1'])
    client.force_authenticate(user=users[tested_user])
    data = {
        "title": "Шкаф IKEA",
        "description": "Срочно"
    }

    response = client.patch(f'/api/advertisements/{adverts[0].id}/', data=data)

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['tested_user', 'expected_status'],
    (
        ('anon', 401),
        ('admin', 204),
        ('user1', 204),
        ('user2', 403),
    )
)
def test_delete(client, advert_factory, users, tested_user, expected_status):
    adverts = advert_factory(_quantity=1, creator=users['user1'])
    client.force_authenticate(user=users[tested_user])

    response = client.delete(f'/api/advertisements/{adverts[0].id}/')

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['tested_user', 'expected_status'],
    (
        ('anon', 401),
        ('admin', 200),
        ('user1', 403),
        ('user2', 200),
    )
)
def test_add_favorite(client, advert_factory, users, tested_user, expected_status):
    adverts = advert_factory(
        _quantity=1,
        creator=users['user1'],
        )
    client.force_authenticate(user=users[tested_user])

    response = client.patch(f'/api/advertisements/{adverts[0].id}/add_favorite/')

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['tested_user', 'count'],
    (
        ('anon', 0),
        ('admin', 0),
        ('user1', 1),
        ('user2', 0),
    )
)
def test_list_status(client, advert_factory, users, tested_user, count):
    adverts = advert_factory(
        _quantity=1,
        creator=users['user1'],
        status='DRAFT',
    )
    client.force_authenticate(user=users[tested_user])

    response = client.get('/api/advertisements/')

    assert len(response.json()) == count
