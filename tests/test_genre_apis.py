import base64
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
# import os, django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibMangSysPrj.settings")
# django.setup()

endpoints={
    "genre": "/genres",
    "lang": "/languages",
    "book": "/books",
    "book_ins": "/book_instances",
    "auth": "/authors"
}

def getAuthstr(username, password):
    credentials_base64 = base64.b64encode(f"{username}:{password}".encode()).decode('utf-8')

    # Construct the Authorization header
    auth_str= f"Basic {credentials_base64}"
    return auth_str

def create_genre(client, payload):
    url = endpoints.get('genre')
    return client.post(url, payload, format='json')

def get_genres(client):
    url = endpoints.get('genre')
    return client.get(url)

def get_genres_by_id(client, id):
    url = endpoints.get('genre') + f"?id={id}"
    return client.get(url)

def delete_genres_by_id(client, id):
    url = endpoints.get('genre') + f"?id={id}"
    return client.delete(url)

def update_genres_by_id(client, id, payload):
    url = endpoints.get('genre') + f"?id={id}"
    return client.put(url, payload, format="json")


@pytest.fixture()
def client():
    user = User.objects.create_user(username='test_user', password='user1234', is_staff=True)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=getAuthstr("test_user","user1234"))
    return client


@pytest.fixture()
def demo_data(client):
    create_genre(client, {
        "name": "fiction"
    })
    create_genre(client, {
        "name": "tragedy"
    })
    create_genre(client, {
        "name": "science fiction"
    })


@pytest.mark.django_db
def test_get_genre_endpoint(client, demo_data):
    demo_data
    response = get_genres(client)
    print(response.json())
    assert response.status_code == 200



@pytest.mark.parametrize("payload, status_code", [
    ({
        "name": "science fiction"
     }, 200)
])
@pytest.mark.django_db
def test_create_genre_api_working(client, payload, status_code):
    response=create_genre(client, payload)

    assert response.status_code == status_code
    response=response.json()
    data=get_genres(client).json()
    assert len(data)==1


@pytest.mark.parametrize("id, status_code", [
    (6, 200),    # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db
def test_get_genre_by_id(demo_data, client, id, status_code):
    demo_data
    print(get_genres(client).json())
    response=get_genres_by_id(client, id)
    print(response.json())
    assert response.status_code==status_code


@pytest.mark.parametrize("id, status_code", [
    (14, 204),    # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db
def test_delete_genre_by_id(demo_data, client, id, status_code):
    demo_data
    response =delete_genres_by_id(client, id)
    print(get_genres(client).json())
    assert response.status_code == status_code


@pytest.mark.parametrize("id, status_code, payload", [
    (23, 200, {
        "name": "classic"
    })
])
@pytest.mark.django_db
def test_update_genre_by_id(client, demo_data, id, status_code, payload):
    demo_data
    response = update_genres_by_id(client, id, payload)
    assert response.status_code == status_code


