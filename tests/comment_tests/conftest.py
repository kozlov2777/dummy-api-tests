import pytest


@pytest.fixture
def create_and_after_delete_user(user, post):
    data_user = {
        "title": "mr",
        "firstName": "TestFirstName2",
        "lastName": "TestLastName2",
        "picture": "https://randomuser.me/api/portraits/med/women/89.jpg",
        "gender": "female",
        "email": "testmail32171@example.com",
        "dateOfBirth": "1956-04-15T00:10:35.555Z",
        "phone": "(019)-646-0430",
        "location": {
            "street": "1371, Dilledonk-Zuid",
            "city": "Den Bommel",
            "state": "Gelderland",
            "country": "Netherlands",
            "timezone": "-5:00",
        },
        "registerDate": "2021-06-21T21:02:07.533Z",
        "updatedDate": "2021-06-21T21:02:07.533Z",
    }
    response_create = user.create_user(data=data_user)

    yield response_create

    user.delete_user(response_create.json()["id"])


@pytest.fixture
def create_post_and_after_delete(post, create_and_after_delete_user):
    id_user = create_and_after_delete_user.json()["id"]
    data_post = {
        "text": "Some Post",
        "image": "https://randomuser.me/api/portraits/med/women/89.jpg",
        "likes": 4,
        "tags": ["dog", "cat"],
        "owner": id_user,
    }
    response_create_post = post.create_post(data=data_post)
    yield response_create_post
    id_post = response_create_post.json()["id"]
    post.delete_post(post_id=id_post)


@pytest.fixture
def create_comment(comment, create_and_after_delete_user, create_post_and_after_delete):
    id_user = create_and_after_delete_user.json()["id"]
    id_post = create_post_and_after_delete.json()["id"]
    data = {"message": "Test comment", "owner": id_user, "post": id_post}
    response = comment.create_comment(data=data)
    yield response
