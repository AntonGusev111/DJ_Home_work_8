import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/?course_id=', data={'course_id': {course[0].id}})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == course[0].id


@pytest.mark.django_db
def test_list_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/?course_id=', data={'course_id': {courses[0].id}})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?course_name={courses[0].name}')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    Student.objects.create(name='name', birth_date="2000-02-02")
    stud = Student.objects.get(name='name')
    response = client.post('/api/v1/courses/', data={"name": "name", "students": [stud.id]}, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'name'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
