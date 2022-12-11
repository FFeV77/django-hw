import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve(client, course_factory):
    course = course_factory(_quantity=1)

    request = client.get(f'/api/v1/courses/{course[0].id}/')
    data = request.json()

    assert request.status_code == 200
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_get(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get('/api/v1/courses/')
    data = request.json()

    assert request.status_code == 200
    for i, m in enumerate(data):
        assert m['name'] == course[i].name


@pytest.mark.django_db
def test_id_filter(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get(f'/api/v1/courses/?id={course[5].id}')
    data = request.json()

    assert request.status_code == 200
    assert data[0]['name'] == course[5].name


@pytest.mark.django_db
def test_name_filter(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get(f'/api/v1/courses/?name={course[5].name}')
    data = request.json()

    assert request.status_code == 200
    assert data[0]['name'] == course[5].name


@pytest.mark.django_db
def test_create(client):
    data = {
        'name': 'test_course',
    }

    request = client.post('/api/v1/courses/', data=data)
    check_req = client.get(f'/api/v1/courses/?name={data["name"]}')
    resp = check_req.json()

    assert request.status_code == 201
    assert len(resp) == 1
    assert resp[0]['name'] == data['name']


@pytest.mark.django_db
def test_update(client, course_factory):
    course = course_factory(_quantity=1)
    data = {
        'name': 'updated_name',
    }

    request = client.patch(f'/api/v1/courses/{course[0].id}/', data=data)
    check_req = client.get(f'/api/v1/courses/{course[0].id}/')
    resp = check_req.json()

    assert request.status_code == 200
    assert check_req.status_code == 200
    assert resp['name'] == data['name']


@pytest.mark.django_db
def test_delete(client, course_factory):
    course = course_factory(_quantity=1)

    request = client.delete(f'/api/v1/courses/{course[0].id}/')
    check_req = client.get(f'/api/v1/courses/{course[0].id}/')

    assert request.status_code == 204
    assert check_req.status_code == 404


@pytest.mark.parametrize(
    ['data', 'expected_code'],
    (
        ({
            'name': 'test_course',
            'students': 11,
        }, 400),
        ({
            'name': 'test_course',
        }, 201),
    )
)
@pytest.mark.django_db
def test_limit(client, settings, data, expected_code):
    settings.MAX_STUDENTS_PER_COURSE = 0

    request = client.post('/api/v1/courses/', data=data)

    assert request.status_code == expected_code
