import allure
import pytest
from framework.responses.user_responses.user_preview import UserPreview
from framework.responses.user_responses.user_full import UserFull
from utils.pydantic_validators import response_validator


class TestUser:
    @allure.title("Get list of users")
    @allure.feature("GET /user")
    def test_get_user_list(self, user):
        params = None
        response = user.list_of_users(params=params)
        response_validator(model=UserPreview, response=response, index_post_preview=0)
        response_validator(model=UserPreview, response=response, index_post_preview=1)
        assert response.status_code == 200

    @allure.title("Checking length of page equals limit")
    @allure.feature("GET /user")
    def test_get_user_list_(self, user):
        response = user.list_of_users(None)
        len_list = len(response.json()["data"])
        assert len_list == int(response.json()["limit"])

    @allure.title("Test defaults value of limit")
    @allure.feature("GET /user")
    @pytest.mark.parametrize(
        "limit, result",
        [
            pytest.param(4, 5, id="test min length-1"),
            pytest.param(51, 50, id="test max length+1"),
            pytest.param(25, 25, id="test valid length"),
        ],
    )
    def test_get_user_list_limit(self, user, limit, result):
        params = {"limit": limit}
        response = user.list_of_users(params=params)
        len_list = len(response.json()["data"])
        assert len_list == result

    @allure.feature("GET /user")
    @pytest.mark.parametrize(
        "page, result",
        [
            pytest.param(-1, 20, id="Test invalid number page return firs page"),
            pytest.param(
                "some_value",
                20,
                id="Test invalid format (str) of number page return firs page",
            ),
            pytest.param(1, 20, id="Test valid page"),
            pytest.param(99999, 0, id="Test invalid page max length return empty list"),
        ],
    )
    def test_get_user_list_pages(self, user, page, result):
        params = {"page": page}
        response = user.list_of_users(params=params)
        len_list = len(response.json()["data"])
        assert len_list == result

    @allure.title("Get info by id")
    @allure.feature("GET /user/id")
    def test_get_user_by_id(self, get_user_and_delete_after_test, user):
        id_user = get_user_and_delete_after_test.json()["id"]
        response = user.get_user_by_id(id_user=id_user)
        assert response.json()["firstName"] == "TestFirstName2"
        assert response.json()["phone"] == "(019)-646-0430"
        assert response.status_code == 200

    @allure.title("Checking format get user by id")
    @allure.feature("GET /user/id")
    def test_get_user_by_id_format(self, get_user_and_delete_after_test, user):
        id_user = get_user_and_delete_after_test.json()["id"]
        response = user.get_user_by_id(id_user=id_user)
        response_validator(model=UserFull, response=response)

    @allure.title("Get info by invalid id")
    @allure.feature("GET /user/id")
    def test_get_user_by_invalid_id(self, user):
        response = user.get_user_by_id("some_id")
        assert response.json()["error"] == "PARAMS_NOT_VALID"
        assert response.status_code == 400

    @allure.feature("PUT /user/id")
    @pytest.mark.parametrize(
        "key, value",
        [
            pytest.param(
                "firstName", "Updated first name", id="Test update first name"
            ),
            pytest.param("lastName", "Updated lastName", id="Test update last name"),
            pytest.param(
                "picture",
                '"https://randomuser.me/api/portraits/med/women/6.jpg"',
                id="Test update picture",
            ),
            pytest.param("gender", "male", id="Test update gender"),
            pytest.param(
                "dateOfBirth", "1990-03-04T03:04:53.673Z", id="Test update birthday"
            ),
            pytest.param("phone", "(319)-646-0430", id="Test update phone"),
            pytest.param(
                "location",
                {
                    "street": "4162, Rua da Paz ",
                    "city": "Test ",
                    "state": "Tets state",
                    "country": "Ukraine",
                    "timezone": "-4:00",
                },
                id="Test update location",
            ),
        ],
    )
    def test_update_user(self, get_user_and_delete_after_test, user, key, value):
        id_user = get_user_and_delete_after_test.json()["id"]
        data = {key: value}
        response = user.update_user(id_user=id_user, data=data)
        assert response.status_code == 200
        assert response.json()[key] == value

    @allure.feature("PUT /user/id")
    @pytest.mark.parametrize(
        "key, value",
        [
            pytest.param("firstName", 1, id="Test update first name invalid (int)"),
            pytest.param(
                "firstName", False, id="Test update first name invalid (Boolean)"
            ),
            pytest.param("firstName", [], id="Test update first name invalid (List)"),
            pytest.param("lastName", 1, id="Test update last name invalid (int)"),
            pytest.param(
                "lastName", True, id="Test update last name invalid (Boolean)"
            ),
            pytest.param("lastName", [], id="Test update last name invalid (List)"),
            pytest.param("picture", 1, id="Test update picture invalid (int)"),
            pytest.param("picture", [], id="Test update picture invalid (List)"),
            pytest.param("picture", False, id="Test update picture invalid (Boolean)"),
            pytest.param("gender", 1, id="Test update gender invalid (int)"),
            pytest.param("gender", [], id="Test update gender invalid (List)"),
            pytest.param("gender", False, id="Test update gender invalid (Boolean)"),
            pytest.param("dateOfBirth", 1, id="Test update birthday invalid (int)"),
            pytest.param("dateOfBirth", [], id="Test update birthday invalid (List)"),
            pytest.param(
                "dateOfBirth", [], id="Test update birthday invalid (Boolean)"
            ),
            pytest.param("phone", 3196460430, id="Test update phone invalid (int)"),
            pytest.param("phone", [], id="Test update phone invalid (List)"),
            pytest.param("phone", False, id="Test update phone invalid (Boolean)"),
            pytest.param(
                "location",
                {"street": 1, "city": 1, "state": 1, "country": 1, "timezone": -4},
                id="Test update location invalid (int)",
            ),
            pytest.param(
                "location",
                {
                    "street": True,
                    "city": True,
                    "state": True,
                    "country": True,
                    "timezone": True,
                },
                id="Test update location invalid(Boolean)",
            ),
            pytest.param(
                "location",
                {"street": [], "city": [], "state": [], "country": [], "timezone": []},
                id="Test update location invalid(List)",
            ),
        ],
    )
    def test_update_user_error(self, user, get_user_and_delete_after_test, key, value):
        id_user = get_user_and_delete_after_test.json()["id"]
        data = {key: value}
        response = user.update_user(id_user=id_user, data=data)
        assert response.status_code == 400
        assert response.json()["error"] == "BODY_NOT_VALID"

    @allure.title("Test delete user")
    @allure.feature("DELETE /user/id")
    def test_delete_user(self, user):
        data = {
            "title": "mr",
            "firstName": "TestFirstName2",
            "lastName": "TestLastName2",
            "picture": "https://randomuser.me/api/portraits/med/women/89.jpg",
            "gender": "female",
            "email": "test_delete123@example.com",
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
        created_user = user.create_user(data=data)
        id_user = created_user.json()["id"]
        response_delete = user.delete_user(id_user=id_user)
        assert response_delete.status_code == 200

    @allure.title("Test delete user invalid (id)")
    @allure.feature("DELETE /user/id")
    def test_delete_user_invalid(self, user):
        response = user.delete_user(id_user="some_id_123")
        assert response.status_code == 400
        assert response.json()["error"] == "PARAMS_NOT_VALID"

    @allure.title("Test created user")
    @allure.feature("POST /user/create")
    @pytest.mark.parametrize(
        "title, first_name, last_name, picture, gender, email, date_of_birth, phone, location",
        [
            pytest.param(
                "ms",
                "TestFirstName2",
                "TestLastName2",
                "https://randomuser.me/api/portraits/women/58.jpg",
                "female",
                "test_dummy@example.com",
                "1997-04-30T19:26:49.610Z",
                "92694011",
                {
                    "street": "9614, SÃ¸ndermarksvej",
                    "city": "Konigsberger",
                    "state": "Borderland",
                    "country": "Denmark",
                    "timezone": "-9:00",
                },
                id="Test create user with all field",
            ),
            pytest.param(
                None,
                "TestFN",
                "TestLN",
                None,
                None,
                "testem1237@gmail.com",
                None,
                None,
                None,
                id="Test create user with only required field",
            ),
        ],
    )
    def test_create_user(
        self,
        user,
        title,
        first_name,
        last_name,
        picture,
        gender,
        email,
        date_of_birth,
        phone,
        location,
    ):
        data = {
            "title": title,
            "firstName": first_name,
            "lastName": last_name,
            "picture": picture,
            "gender": gender,
            "email": email,
            "dateOfBirth": date_of_birth,
            "phone": phone,
            "location": location,
        }
        response = user.create_user(data=data)
        assert response.status_code == 200
        id_user = response.json()["id"]
        delete = user.delete_user(id_user=id_user)
        assert delete.status_code == 200

    @allure.title("Test created user invalid")
    @allure.feature("POST /user/create")
    @pytest.mark.parametrize(
        "title, first_name, last_name, picture, gender, email, date_of_birth, phone, location",
        [
            pytest.param(
                "mr",
                None,
                "TestLN",
                "https://randomuser.me/api/portraits/women/58.jpg",
                "male",
                "testem123@gmail.com",
                "1996-04-30T19:26:49.610Z",
                "92694011",
                [
                    "9614, SÃ¸ndermarksvej",
                    "Konigsberger",
                    "Borderland",
                    "Denmark",
                    "-9:00",
                ],
                id="Test create user invalid first name(None)",
            ),
            pytest.param(
                "mr",
                "TestFN",
                None,
                "https://randomuser.me/api/portraits/women/58.jpg",
                "male",
                "testem123@gmail.com",
                "1996-04-30T19:26:49.610Z",
                "92694011",
                [
                    "9614, SÃ¸ndermarksvej",
                    "Kongsvinger",
                    "Nordjylland",
                    "Denmark",
                    "-9:00",
                ],
                id="Test create user invalid last name(None)",
            ),
            pytest.param(
                "mr",
                "TestFN",
                "TestLN",
                "https://randomuser.me/api/portraits/women/58.jpg",
                "male",
                None,
                "1996-04-30T19:26:49.610Z",
                "92694011",
                [
                    "9614, SÃ¸ndermarksvej",
                    "Kongsvinger",
                    "Nordjylland",
                    "Denmark",
                    "-9:00",
                ],
                id="Test create user invalid email(None)",
            ),
        ],
    )
    def test_create_user_invalid(
        self,
        user,
        title,
        first_name,
        last_name,
        picture,
        gender,
        email,
        date_of_birth,
        phone,
        location,
    ):
        data = {
            "title": title,
            "firstName": first_name,
            "lastName": last_name,
            "picture": picture,
            "gender": gender,
            "email": email,
            "dateOfBirth": date_of_birth,
            "phone": phone,
            "location": location,
        }
        response = user.create_user(data=data)
        assert response.status_code == 400
        assert response.json()["error"] == "BODY_NOT_VALID"
