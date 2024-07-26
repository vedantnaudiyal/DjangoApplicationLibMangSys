import base64
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient



endpoints={
    "genre": "/genres",
    "lang": "/languages",
    "book": "/books",
    "book_ins": "/bookInstances",
    "auth": "/authors",
    "late_sub": "/getBookInstancesLateSubmission",
    "book_by_status": "/getBookInstancesByStatus"
}

def getAuthstr(username, password):
    credentials_base64 = base64.b64encode(f"{username}:{password}".encode()).decode('utf-8')
    auth_str= f"Basic {credentials_base64}"
    return auth_str

def create_book_ins(client, payload):
    url = endpoints.get('book_ins')
    return client.post(url, payload, format='json')

def get_book_ins(client):
    url = endpoints.get('book_ins')
    return client.get(url)

def get_book_ins_by_id(client, id):
    url = endpoints.get('book_ins') + f"?id={id}"
    return client.get(url)

def delete_book_ins_by_id(client, id):
    url = endpoints.get('book_ins') + f"?id={id}"
    return client.delete(url)

def update_book_ins_by_id(client, id, payload):
    url = endpoints.get('book_ins') + f"?id={id}"
    return client.put(url, payload, format="json")

def create_book(client, payload):
    url = endpoints.get('book')
    return client.post(url, payload, format='json')


@pytest.fixture()
def client():
    user = User.objects.create_user(username='test_user', password='user1234', is_staff=True)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=getAuthstr("test_user","user1234"))
    return client



@pytest.fixture()
def demo_data(client):
    genre1=client.post(endpoints.get('genre'), {
        "name": "fiction"
    }, format='json').json()

    print(genre1)
    lang1 = client.post(endpoints.get('lang'), {
        "name": "hindi"
    }, format='json').json()
    auth=client.post(endpoints.get('auth'), {
        "name": "Premchand"
    }, format='json').json()
    book=create_book(client, {
        "title": "To Kill a Mockingbird",
        "summary": "Set in the American South during the 1930s, this novel explores themes of racial injustice and moral growth through the eyes of Scout Finch, a young girl whose father, Atticus Finch, defends a black man falsely accused of raping a white woman.",
        "ISBN": "0061120081",
        "author": auth['id'],
        "language": lang1['id'],
        "genre": [
            genre1['id']
        ]
    }).json()
    book_ins1=create_book_ins(client, {
        "return_date": "2024-11-01",
        "book_status": "b",
        "book": book['id']
    }).json()
    book_ins2 = create_book_ins(client, {
        "return_date": None,
        "book": book['id']
    }).json()
    print(book, book_ins2, book_ins1)
    # print(b2.json())



@pytest.mark.django_db(reset_sequences=True)
def test_get_book_endpoint(client, demo_data):

    response = get_book_ins(client)

    # print(response.json())
    assert response.status_code == 200



@pytest.mark.parametrize("payload, status_code", [
    ({
        "return_date": "2024-12-01",
        "book_status": "b",
        "book": 1
    }, 201),    # ok status
    ({
        "return_date": "2024-12-01",
        "book_status": "b"
    }, 400),    # bad request body fields
    ({
        "return_date": "2024-12-01",
        "book_status": "z"  # invalid choice field
    }, 400),
])
@pytest.mark.django_db(reset_sequences=True)
def test_create_book_ins_api_working(client,demo_data, payload, status_code):
    response=create_book_ins(client, payload)
    print(response.json())
    assert response.status_code == status_code


# -------------------------- negative testing ------------------------
@pytest.mark.django_db(reset_sequences=True)
def test_create_book_ins_unique_id_already_exists(client, demo_data):
    book_ins=create_book_ins(client, {
        "return_date": "2024-12-01",
        "book_status": "b",
        "book": 1
    })
    response=create_book_ins(client, {
        "unique_id": book_ins.get('unique_id'),
        "book": 1
    })
    print(response.json())
    assert response.status_code == 400

# #
# #
#
@pytest.mark.parametrize("id, status_code", [
    (999, 404),  # Non-existent
    ("dejudfuyghukhjghkj98756689ytf-ftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_get_book_ins_by_id(client, id, status_code):
    response=get_book_ins_by_id(client, id)
    # print(response.json())
    assert response.status_code==status_code
# #
# #
# cascade deletion -> if book deleted no problem but if genre, lan or author deleted book also deleted
@pytest.mark.parametrize("id, status_code", [
    (999, 404),  # Non-existent book ID
    ("deftf", 404)
])
@pytest.mark.django_db(reset_sequences=True)
def test_delete_book_by_id(client, id, status_code):
    response =delete_book_ins_by_id(client, id)
    # print(get_book_ins_by_id(client).json())
    assert response.status_code == status_code

#     TODO GET AND DELETE BOOK_INSTNACE BY VALID UNIQUE_ID AND SHOW PROTECT FEATURE

# --------- positive get del upd-----------
@pytest.mark.django_db(reset_sequences=True)
def test_get_del_upd_book_ins_by_id(client, demo_data):
    book_ins=create_book_ins(client,{
        "return_date": "2024-12-01",
        "book_status": "b",
        "book": 1
    }).json()
    print(book_ins)
    response=get_book_ins_by_id(client, book_ins['unique_id'])
    # print(response.json())
    assert response.status_code==200
    response = update_book_ins_by_id(client, book_ins['unique_id'], {
        "book_status": "a"
    })
    # print(response.json())
    assert response.status_code == 200
    response = delete_book_ins_by_id(client, book_ins['unique_id'])
    # print(response.json())
    assert response.status_code == 204



# ----------------------
@pytest.mark.django_db(reset_sequences=True)
def test_get_late_submissions(demo_data, client):
    demo_data
    response=client.get(endpoints.get("late_sub"))
    print(response.json())

    assert response.status_code==200



@pytest.mark.parametrize("status, status_code", [
    ('b', 200),  # Non-existent book ID
    ('a', 200),
    ('z', 400)   # non existent
    ])
@pytest.mark.django_db(reset_sequences=True)
def test_get_books_by_status(demo_data, client, status, status_code):
    demo_data
    response = client.get(endpoints.get("book_by_status")+f"?status={status}")
    print(response.json())

    assert response.status_code == status_code