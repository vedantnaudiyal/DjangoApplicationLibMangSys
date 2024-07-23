import base64
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

endpoints={
    "genre": "/genres",
    "lang": "/languages",
    "book": "/books",
    "book_ins": "/book_instances",
    "auth": "/authors"
}

def getAuthstr(username, password):
    credentials_base64 = base64.b64encode(f"{username}:{password}".encode()).decode('utf-8')
    auth_str= f"Basic {credentials_base64}"
    return auth_str

def create_book(client, payload):
    url = endpoints.get('book')
    return client.post(url, payload, format='json')

def create_genre(client, payload):
    url = endpoints.get('genre')
    return client.post(url, payload, format='json')

def create_language(client, payload):
    url = endpoints.get('lang')
    return client.post(url, payload, format='json')

def get_books(client):
    url = endpoints.get('book')
    return client.get(url)

def get_books_by_id(client, id):
    url = endpoints.get('book') + f"?id={id}"
    return client.get(url)

def delete_books_by_id(client, id):
    url = endpoints.get('book') + f"?id={id}"
    return client.delete(url)

def update_books_by_id(client, id, payload):
    url = endpoints.get('book') + f"?id={id}"
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
        "name": "modern literature"
    })
    create_language(client, {
        "name": "english"
    })
    create_language(client, {
        "name": "hindi"
    })
    create_book(client, {
        "title": "To Kill a Mockingbird",
        "summary": "Set in the American South during the 1930s, this novel explores themes of racial injustice and moral growth through the eyes of Scout Finch, a young girl whose father, Atticus Finch, defends a black man falsely accused of raping a white woman.",
        "ISBN": "0061120081",
        "author": 2,
        "language": 1,
        "genre": [
            2
        ]
    })
    create_book(client, {
        "title": "Godan",
        "summary": "A classic Hindi novel that portrays the struggles of a poor farmer, Hori, and his aspiration to fulfill his dream of owning a cow (Godan) in pre-independence India. It delves into themes of social inequality, poverty, and the human spirit.",
        "ISBN": "9788126308037",
        "author": 1,
        "language": 2,
        "genre": []
    })


demo_data

@pytest.mark.django_db
def test_get_book_endpoint(client, demo_data):
    response=create_book(client, {
        "id": 5,
        "title": "The Great GatsbyUPD",
        "summary": "A Great Gatsby is a novel by F. Scott Fitzgerald that portrays the American Dream through the life of Jay Gatsby and his pursuit of wealth and love during the Jazz Age. It explores themes of decadence, idealism, resistance to change, social upheaval, and excess.",
        "ISBN": "9780743272565",
        "author": 1,
        "language": 1,
        "genre": [
            1
        ]
    })
    print(response.json())
    response = get_books(client)
    print(response.json())
    assert response.status_code == 200



# @pytest.mark.parametrize("payload, status_code", [
#     ({
#         "name": "science fiction"
#      }, 200)
# ])
# @pytest.mark.django_db
# def test_create_book_api_working(client, payload, status_code):
#     response=create_book(client, payload)
#
#     assert response.status_code == status_code
#     response=response.json()
#     data=get_books(client).json()
#     assert len(data)==1
#
#
# @pytest.mark.parametrize("id, status_code", [
#     (6, 200),    # Valid
#     (999, 404),  # Non-existent
#     ("deftf", 404)
# ])
# @pytest.mark.django_db
# def test_get_book_by_id(demo_data, client, id, status_code):
#     demo_data
#     print(get_books(client).json())
#     response=get_books_by_id(client, id)
#     print(response.json())
#     assert response.status_code==status_code
#
#
# @pytest.mark.parametrize("id, status_code", [
#     (14, 204),    # Valid book ID
#     (999, 404),  # Non-existent book ID
#     ("deftf", 404)
# ])
# @pytest.mark.django_db
# def test_delete_book_by_id(demo_data, client, id, status_code):
#     demo_data
#     response =delete_books_by_id(client, id)
#     print(get_books(client).json())
#     assert response.status_code == status_code
#
#
# @pytest.mark.parametrize("id, status_code, payload", [
#     (23, 200, {
#         "name": "classic"
#     })
# ])
# @pytest.mark.django_db
# def test_update_book_by_id(client, demo_data, id, status_code, payload):
#     demo_data
#     response = update_books_by_id(client, id, payload)
#     assert response.status_code == status_code


