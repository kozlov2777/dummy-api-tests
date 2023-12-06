import pytest


@pytest.fixture
def get_user_and_delete_after_test(user):
    data = {
        "title": "mr",
        "firstName": "TestFirstName2",
        "lastName": "TestLastName2",
        "picture": "https://randomuser.me/api/portraits/med/women/89.jpg",
        "gender": "female",
        "email": "test99812434da@example.com",
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
    response = user.create_user(data=data)
    yield response
    user.delete_user(id_user=response.json()["id"])
