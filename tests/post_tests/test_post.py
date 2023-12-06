import allure
import pytest
from framework.responses.post_responses.post_preview import PostPreview
from utils.pydantic_validators import response_validator


class TestPost:
    @allure.title("Get list of posts")
    @allure.feature("GET /post")
    @allure.description(
        "This test checks the request for a list of posts, verifies that all elements match the response model"
    )
    def test_get_posts_list(self, post):
        response = post.get_list_of_posts(params=None)
        response_validator(response=response, index_post_preview=0, model=PostPreview)
        response_validator(response=response, index_post_preview=19, model=PostPreview)
        assert response.status_code == 200

    @allure.feature("GET /post")
    @allure.description(
        "This test check pagination of the request for a list of posts, verifies that its work correctly,"
        " if we enter invalid integer values of limit"
    )
    @pytest.mark.parametrize(
        "limit, result",
        [
            pytest.param(4, 5, id="test get_post_list_pagination min limit -1"),
            pytest.param(51, 50, id="test get_post_list_pagination max limit +1"),
            pytest.param(25, 25, id="test get_post_list_pagination limit"),
        ],
    )
    def test_get_post_list_pagination(self, post, limit, result):
        params = {"limit": limit}
        response = post.get_list_of_posts(params=params)
        len_list = len(response.json()["data"])
        assert len_list == result

    @allure.feature("GET /post")
    @allure.description(
        "This test check pagination of the request for a list of posts, we check that if enter wrong format for limit,"
        " we get default values for it(null)"
    )
    @pytest.mark.parametrize(
        "limit",
        [
            pytest.param("limit", id="test get_post_list_pagination wrong format(str)"),
            pytest.param(
                False, id="test get_post_list_pagination wrong format(boolean)"
            ),
        ],
    )
    def test_get_post_list_pagination_error(self, post, limit):
        params = {"limit": limit}
        response = post.get_list_of_posts(params=params)
        assert response.json()["limit"] is None

    @allure.feature("GET /post")
    @pytest.mark.parametrize(
        "page, result",
        [
            pytest.param(-1, 0, id="test get list post page if page = -1"),
            pytest.param("sfd", None, id="test get list post page if page is str"),
            pytest.param(True, None, id="test get list post page if page is True"),
        ],
    )
    def test_get_post_list_page_wrong_format(self, post, page, result):
        params = {"page": page}
        response = post.get_list_of_posts(params=params)
        assert response.json()["page"] == result

    @allure.feature("GET /post")
    @pytest.mark.parametrize(
        "first_page, second_page",
        [pytest.param(0, 2, id="test get list of post page valid")],
    )
    def test_get_post_list_page(self, post, first_page, second_page):
        param1 = {"page": first_page}
        param2 = {"page": second_page}
        response_page_one = post.get_list_of_posts(params=param1)
        response_page_two = post.get_list_of_posts(params=param2)
        first_id_from_first_page = response_page_one.json()["data"][0]["id"]
        first_id_from_second_page = response_page_two.json()["data"][0]["id"]
        assert first_id_from_first_page != first_id_from_second_page

    @allure.feature("GET /user/id/post")
    @allure.title("Get list of post by user id")
    def test_get_post_by_user_id(self, post):
        response = post.get_post_by_user_id("60d0fe4f5311236168a109e2")
        response_validator(response=response, index_post_preview=0, model=PostPreview)
        response_validator(response=response, index_post_preview=-1, model=PostPreview)
        assert response.status_code == 200

    @allure.feature("GET /user/id/post")
    @allure.title("Get list of post by wrong user id Error")
    def test_get_post_by_user_id_error(self, post):
        response = post.get_post_by_user_id("test_id_123")
        assert response.status_code == 400
        assert response.json()["error"] == "PARAMS_NOT_VALID"

    @allure.feature("GET /tag/id/post")
    @allure.title("Get list of post by tag id")
    def test_get_post_by_tag_id(self, post):
        response = post.get_list_of_post_by_tag("sweden")
        response_validator(response=response, index_post_preview=0, model=PostPreview)
        response_validator(response=response, index_post_preview=-1, model=PostPreview)
        assert response.status_code == 200

    @allure.feature("GET /user/id/post")
    @allure.title("Get list of post by wrong tag id Error")
    def test_get_post_by_user_id_error(self, post):
        response = post.get_list_of_post_by_tag("some_tag_132")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0

    @allure.feature("GET /post/id")
    @allure.title("Get post by id")
    def test_get_post(self, create_and_after_delete_user, post):
        id_user = create_and_after_delete_user.json()["id"]
        data_post = {
            "text": "some text",
            "image": "https://img.dummyapi.io/photo-1524675772159-ea8ff66a947d.jpg",
            "likes": 2,
            "tags": [
                "sled",
                "dogsled",
            ],
            "owner": id_user,
        }
        response_create_post = post.create_post(data=data_post)
        response = post.get_post_by_id(response_create_post.json()["id"])
        response_validator(response=response, index_post_preview=0, model=PostPreview)
        assert response.status_code == 200

    @allure.feature("GET /post/id")
    @allure.title("Get post by id ERROR")
    def test_get_post_error(self, post):
        response = post.get_post_by_id("some_post_id")
        assert response.status_code == 400
        assert response.json()["error"] == "PARAMS_NOT_VALID"

    @allure.feature("POST /post/create")
    @pytest.mark.parametrize(
        "text, image,likes,tags",
        [
            pytest.param(
                "Test text",
                "https://img.dummyapi.io/photo-1524675772159-ea8ff66a947d.jpg",
                2,
                ["dog", "cat"],
                id="Test create post valid",
            ),
            pytest.param(
                "Test text",
                None,
                None,
                None,
                id="Test create post valid only required ",
            ),
        ],
    )
    def test_create_post(
        self, post, create_and_after_delete_user, text, image, likes, tags
    ):
        id_user = create_and_after_delete_user.json()["id"]
        data_post = {
            "text": text,
            "image": image,
            "likes": likes,
            "tags": tags,
            "owner": id_user,
        }
        response_create_post = post.create_post(data=data_post)
        response_validator(response=response_create_post, model=PostPreview)
        assert response_create_post.status_code == 200

    @allure.feature("POST /post/create")
    @pytest.mark.parametrize(
        "text, image,likes,tags",
        [
            pytest.param(
                None,
                "https://img.dummyapi.io/photo-1524675772159-ea8ff66a947d.jpg",
                2,
                ["dog", "cat"],
                id="Test create post ERROR without required field(title)",
            ),
        ],
    )
    def test_create_post_error(
        self, post, create_and_after_delete_user, text, image, likes, tags
    ):
        id_user = create_and_after_delete_user.json()["id"]
        data_post = {
            "text": text,
            "image": image,
            "likes": likes,
            "tags": tags,
            "owner": id_user,
        }
        response_create_post = post.create_post(data=data_post)
        assert response_create_post.status_code == 400
        assert response_create_post.json()["error"] == "BODY_NOT_VALID"

    @allure.feature("POST /post/create")
    @pytest.mark.parametrize(
        "text, image,likes,tags",
        [
            pytest.param(
                "Test text",
                "https://img.dummyapi.io/photo-1524675772159-ea8ff66a947d.jpg",
                2,
                ["dog", "cat"],
                id="Test create post ERROR without required field(owner)",
            ),
        ],
    )
    def test_create_post_error_owner(self, post, text, image, likes, tags):
        data_post = {
            "text": text,
            "image": image,
            "likes": likes,
            "tags": tags,
            "owner": None,
        }
        response_create_post = post.create_post(data=data_post)
        assert response_create_post.status_code == 400
        assert response_create_post.json()["error"] == "BODY_NOT_VALID"

    @allure.feature("PUT /post/id")
    @pytest.mark.parametrize(
        "text, image, likes, tags",
        [
            pytest.param(
                "Updated text",
                "https://img.dummyapi.io/photo-1524675772159-ea8ff66a147d.jpg",
                10,
                ["update"],
                id="Test update post",
            )
        ],
    )
    def test_update_post(
        self, post, create_post_and_after_delete, text, image, likes, tags
    ):
        id_post = create_post_and_after_delete.json()["id"]
        data_for_update = {
            "text": text,
            "image": image,
            "likes": likes,
            "tags": tags,
        }
        response = post.update_post(post_id=id_post, data=data_for_update)
        response_validator(response=response, model=PostPreview)
        assert response.status_code == 200

    @allure.feature("PUT /post/id")
    @pytest.mark.parametrize(
        "text, image, likes, tags",
        [
            pytest.param(
                "Updated text",
                "https://img.dummyapi.io/photo-1524675772159-ea8ff66a147d.jpg",
                "a",
                ["update"],
                id="Test update post error (likes is str)",
            )
        ],
    )
    def test_update_post_error_format_field(
        self, post, create_post_and_after_delete, text, image, likes, tags
    ):
        id_post = create_post_and_after_delete.json()["id"]
        data_for_update = {"text": text, "image": image, "likes": likes, "tags": tags}
        response = post.update_post(post_id=id_post, data=data_for_update)
        assert response.status_code == 400
        assert response.json()["error"] == "BODY_NOT_VALID"
