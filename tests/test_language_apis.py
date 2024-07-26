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


def create_lang(client, payload):
    url = endpoints.get('lang')
    return client.post(url, payload, format='json')


def get_langs(client):
    url = endpoints.get('lang')
    return client.get(url)


def get_langs_by_id(client, id):
    url = endpoints.get('lang') + f"?id={id}"
    return client.get(url)


def delete_langs_by_id(client, id):
    url = endpoints.get('lang') + f"?id={id}"
    return client.delete(url)


def update_langs_by_id(client, id, payload):
    url = endpoints.get('lang') + f"?id={id}"
    return client.put(url, payload, format="json")


@pytest.fixture()
def client():
    user = User.objects.create_user(username='test_user', password='user1234', is_staff=True)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=getAuthstr("test_user", "user1234"))
    return client


@pytest.fixture()
def demo_data(client):
    create_lang(client, {
        "name": "hindi"
    })
    create_lang(client, {
        "name": "english"
    })
    create_lang(client, {
        "name": "french"
    })


@pytest.mark.django_db(reset_sequences=True)
def test_get_lang_endpoint(client, demo_data):
    response = get_langs(client)
    print(response.json())
    assert response.status_code == 200


@pytest.mark.parametrize("payload, status_code", [
    ({
         "name": "spanish"
     }, 200)
])
@pytest.mark.django_db(reset_sequences=True)
def test_create_lang_api_working(client, payload, status_code):
    response = create_lang(client, payload)
#
    assert response.status_code == status_code
    response = response.json()
    data = get_langs(client).json()
    assert len(data) == 1
#
#
@pytest.mark.parametrize("id, status_code", [
    (1, 200),  # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_get_lang_by_id(demo_data, client, id, status_code):
    print(get_langs(client).json())
    response = get_langs_by_id(client, id)
    print(response.json())
    assert response.status_code == status_code
#
#
@pytest.mark.parametrize("id, status_code", [
    (1, 204),  # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404),
    ('', 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_delete_lang_by_id(demo_data, client, id, status_code):
    response = delete_langs_by_id(client, id)
    print(get_langs(client).json())
    assert response.status_code == status_code
#
#
@pytest.mark.parametrize("id, status_code, payload", [
    (1, 200, {
        "name": "spanish"
    })
])
@pytest.mark.django_db(reset_sequences=True)
def test_update_lang_by_id(client, demo_data, id, status_code, payload):
    response = update_langs_by_id(client, id, payload)
    print(response.json())
    assert response.status_code == status_code
