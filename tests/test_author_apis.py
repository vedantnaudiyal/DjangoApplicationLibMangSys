import base64
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

endpoints = {
    "genre": "/genres",
    "lang": "/languages",
    "book": "/books",
    "book_ins": "/book_instances",
    "auth": "/authors"
}


def getAuthstr(username, password):
    credentials_base64 = base64.b64encode(f"{username}:{password}".encode()).decode('utf-8')

    auth_str = f"Basic {credentials_base64}"
    return auth_str


def create_author(client, payload):
    url = endpoints.get('auth')
    return client.post(url, payload, format='json')


def get_authors(client):
    url = endpoints.get('auth')
    return client.get(url)


def get_authors_by_id(client, id):
    url = endpoints.get('auth') + f"?id={id}"
    return client.get(url)


def delete_authors_by_id(client, id):
    url = endpoints.get('auth') + f"?id={id}"
    return client.delete(url)


def update_authors_by_id(client, id, payload):
    url = endpoints.get('auth') + f"?id={id}"
    return client.put(url, payload, format="json")


@pytest.fixture()
def client():
    user = User.objects.create_user(username='test_user', password='user1234', is_staff=True)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=getAuthstr("test_user", "user1234"))
    return client




@pytest.fixture()
def demo_data(client):
    create_author(client, {
        "name": "Premchand",
        "date_of_birth": "2023-11-02",
        "date_of_death": "2024-07-19"
    })
    create_author(client, {
        "name": "Harper Lee",
        "date_of_birth": "2024-01-03",
        "date_of_death": "2024-07-20"
    })
    create_author(client, {
        "name": "J.K. Rowling",
        "date_of_birth": "1965-07-31",
        "date_of_death": None
    })


@pytest.mark.django_db(reset_sequences=True)
def test_get_author_endpoint(client, demo_data):
    response = get_authors(client)
    print(response.json())
    assert response.status_code == 200


@pytest.mark.parametrize("payload, status_code", [
    ({
         "name": "William Shakespeare",
        "date_of_birth": "1564-04-23",
        "date_of_death": "1616-04-23"
     }, 200)
])
@pytest.mark.django_db(reset_sequences=True)
def test_create_author_api_working(client, payload, status_code):
    response = create_author(client, payload)
#
    assert response.status_code == status_code

# #
# #
@pytest.mark.parametrize("id, status_code", [
    (1, 200),  # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_get_author_by_id(demo_data, client, id, status_code):
    print(get_authors(client).json())
    response = get_authors_by_id(client, id)
    print(response.json())
    assert response.status_code == status_code
# #
# #
@pytest.mark.parametrize("id, status_code", [
    (1, 204),  # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404),
    ('', 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_delete_author_by_id(demo_data, client, id, status_code):
    response = delete_authors_by_id(client, id)
    print(get_authors(client).json())
    assert response.status_code == status_code
#
#
@pytest.mark.parametrize("id, status_code, payload", [
    (1, 200, {
        "date_of_death": None
    })
])
@pytest.mark.django_db(reset_sequences=True)
def test_update_author_by_id(client, demo_data, id, status_code, payload):
    response = update_authors_by_id(client, id, payload)
    print(response.json())
    assert response.status_code == status_code
