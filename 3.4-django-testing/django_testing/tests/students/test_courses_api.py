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

# проверка получения первого курса (retrieve-логика)

@pytest.mark.django_db
def test_retrieve(client, course_factory):
    course = course_factory(_quantity=1)

    request = client.get(f'/api/v1/courses/{course[0].id}/')
    data = request.json()

    assert request.status_code == 200
    assert data['name'] == course[0].name

# проверка получения списка курсов (list-логика)

@pytest.mark.django_db
def test_get(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get('/api/v1/courses/')
    data = request.json()

    assert request.status_code == 200
    for i, m in enumerate(data):
        assert m['name'] == course[i].name

# проверка фильтрации списка курсов по id

@pytest.mark.django_db
def test_id_filter(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get(f'/api/v1/courses/?id={course[2].id}')
    data = request.json()

    assert request.status_code == 200
    assert data[0]['name'] == course[2].name

# проверка фильтрации списка курсов по name

@pytest.mark.django_db
def test_name_filter(client, course_factory):
    course = course_factory(_quantity=10)

    request = client.get(f'/api/v1/courses/?name={course[3].name}')
    data = request.json()

    assert request.status_code == 200
    assert data[0]['name'] == course[3].name

# тест успешного создания курса

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

# тест успешного обновления курса

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

# тест успешного удаления курса

@pytest.mark.django_db
def test_delete(client, course_factory):
    course = course_factory(_quantity=1)

    request = client.delete(f'/api/v1/courses/{course[0].id}/')
    check_req = client.get(f'/api/v1/courses/{course[0].id}/')

    assert request.status_code == 204
    assert check_req.status_code == 404
