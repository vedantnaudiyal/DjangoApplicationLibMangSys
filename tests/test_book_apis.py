import base64
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

endpoints={
    "genre": "/genres",
    "lang": "/languages",
    "book": "/books",
    "book_ins": "/book_instances",
    "auth": "/authors",
    "search": "/search_by_title"
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

def create_author(client, payload):
    url = endpoints.get('auth')
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
    genre1=create_genre(client, {
        "name": "fiction"
    }).json()
    genre2=create_genre(client, {
        "name": "modern literature"
    }).json()
    lang1=create_language(client, {
        "name": "english"
    }).json()
    lang2=create_language(client, {
        "name": "hindi"
    }).json()
    auth=create_author(client, {
        "name": "premchand"
    }).json()
    print(genre1, genre2, lang1, lang2)
    b1=create_book(client, {
        "title": "To Kill a Mockingbird",
        "summary": "Set in the American South during the 1930s, this novel explores themes of racial injustice and moral growth through the eyes of Scout Finch, a young girl whose father, Atticus Finch, defends a black man falsely accused of raping a white woman.",
        "ISBN": "0061120081",
        "author": auth['id'],
        "language": lang1['id'],
        "genre": [
            genre2['id']
        ]
    })
    b2=create_book(client, {
        "title": "Godan",
        "summary": "A classic Hindi novel that portrays the struggles of a poor farmer, Hori, and his aspiration to fulfill his dream of owning a cow (Godan) in pre-independence India. It delves into themes of social inequality, poverty, and the human spirit.",
        "ISBN": "9788126308037",
        "author": auth['id'],
        "language": lang2['id'],
        "genre": [
            genre1['id'], genre2['id']
        ]
    })
    # print(b1.json())
    # print(b2.json())



@pytest.mark.django_db(reset_sequences=True)
def test_get_book_endpoint(client, demo_data):

    response = get_books(client)
    # print(response.json())
    assert response.status_code == 200



@pytest.mark.parametrize("payload, status_code", [
    ({
        "title": "The Great GatsbyUPD",
        "summary": "A Great Gatsby is a novel by F. Scott Fitzgerald that portrays the American Dream through the life of Jay Gatsby and his pursuit of wealth and love during the Jazz Age. It explores themes of decadence, idealism, resistance to change, social upheaval, and excess.",
        "ISBN": "9780743272567",
        "author": 1,
        "language": 1,
        "genre": [
            1, 2
        ]
    }, 200),    # ok status
    ({
        "summary": "A Great Gatsby is a novel by F. Scott Fitzgerald that portrays the American Dream through the life of Jay Gatsby and his pursuit of wealth and love during the Jazz Age. It explores themes of decadence, idealism, resistance to change, social upheaval, and excess.",
        "ISBN": "9780743272566",
        "author": 1,
        "genre": [
            1
        ]
    }, 400),    # bad request body fields
    ({
        "title": "The Great GatsbyUPD",
        "summary": "A Great Gatsby is a novel by F. Scott Fitzgerald that portrays the American Dream through the life of Jay Gatsby and his pursuit of wealth and love during the Jazz Age. It explores themes of decadence, idealism, resistance to change, social upheaval, and excess.",
        "ISBN": "9788126308037",
        "author": 1,
        "language": 1,
        "genre": [
            1, 2
        ]
    }, 400)     # same id already exists
])
@pytest.mark.django_db(reset_sequences=True)
def test_create_book_api_working(client,demo_data, payload, status_code):
    response=create_book(client, payload)

    assert response.status_code == status_code
#
#

@pytest.mark.parametrize("id, status_code", [
    (1, 200),    # Valid
    (999, 404),  # Non-existent
    ("deftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_get_book_by_id(demo_data, client, id, status_code):
    print(get_books(client).json())
    response=get_books_by_id(client, id)
    print(response.json())
    assert response.status_code==status_code
#
#
# cascade deletion -> if book deleted no problem but if genre, lan or author deleted book also deleted
@pytest.mark.parametrize("id, status_code", [
    (1, 204),    # Valid book ID
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_delete_book_by_id(demo_data, client, id, status_code):
    response =delete_books_by_id(client, id)
    print(get_books(client).json())
    assert response.status_code == status_code
#
#
@pytest.mark.parametrize("id, status_code, payload", [
    (1, 200, {
        "title": "The Great GatsbyUPD1"
    }),
    (999, 404, {
        "title": "The Great GatsbyUPD1"
    })
])
@pytest.mark.django_db(reset_sequences=True)
def test_update_book_by_id(client, demo_data, id, status_code, payload):
    response = update_books_by_id(client, id, payload)
    assert response.status_code == status_code


@pytest.mark.parametrize("title, status_code", [
    ("", 200),
    ("kill", 200)
])
@pytest.mark.django_db(reset_sequences=True)
def test_search_book_by_title(client, demo_data,title, status_code):
    response = client.get(endpoints.get('search') + f"?title={title}")
    assert response.status_code == status_code


