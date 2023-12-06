import allure
import pytest

from utils.pydantic_validators import response_validator
from framework.responses.comment_responses.comment import Comment


class TestComment:
    @allure.title("Get list of comment")
    @allure.feature("GET /comment")
    @allure.description(
        "This test checks the request for a list of comments, verifies that all elements match the response model"
    )
    def test_get_posts_list(self, comment):
        response = comment.get_list_of_comment(params=None)
        response_validator(response=response, index_post_preview=0, model=Comment)
        response_validator(response=response, index_post_preview=19, model=Comment)
        assert response.status_code == 200

    @allure.feature("GET /comment")
    @allure.description(
        "This test check pagination of the request for a list of comments, verifies that its work correctly,"
        " if we enter invalid integer values of limit"
    )
    @pytest.mark.parametrize(
        "limit, result",
        [
            pytest.param(4, 5, id="test get_comment_list_pagination min limit -1"),
            pytest.param(51, 50, id="test get_comment_list_pagination max limit +1"),
            pytest.param(25, 25, id="test get_comment_list_pagination limit"),
        ],
    )
    def test_get_comment_list_pagination(self, comment, limit, result):
        params = {"limit": limit}
        response = comment.get_list_of_comment(params=params)
        len_list = len(response.json()["data"])
        assert len_list == result

    @allure.feature("GET /post")
    @allure.description(
        "This test check pagination of the request for a list of comments, we check that if enter wrong format for limit,"
        " we get default values for it(null)"
    )
    @pytest.mark.parametrize(
        "limit",
        [
            pytest.param(
                "limit", id="test get_comment_list_pagination wrong format(str)"
            ),
            pytest.param(
                False, id="test get_comment_list_pagination wrong format(boolean)"
            ),
        ],
    )
    def test_get_post_list_pagination_error(self, comment, limit):
        params = {"limit": limit}
        response = comment.get_list_of_comment(params=params)
        assert response.json()["limit"] is None

    @allure.feature("GET /comment")
    @pytest.mark.parametrize(
        "page, result",
        [
            pytest.param(-1, 0, id="test get list comment page if page = -1"),
            pytest.param("sfd", None, id="test get list comment page if page is str"),
            pytest.param(True, None, id="test get list comment page if page is True"),
        ],
    )
    def test_get_post_list_page_wrong_format(self, comment, page, result):
        params = {"page": page}
        response = comment.get_list_of_comment(params=params)
        assert response.json()["page"] == result

    @allure.feature("GET /comment")
    @pytest.mark.parametrize(
        "first_page, second_page",
        [pytest.param(0, 2, id="test get list of comment page valid")],
    )
    def test_get_comment_list_page(self, comment, first_page, second_page):
        param1 = {"page": first_page}
        param2 = {"page": second_page}
        response_page_one = comment.get_list_of_comment(params=param1)
        response_page_two = comment.get_list_of_comment(params=param2)
        first_id_from_first_page = response_page_one.json()["data"][0]["id"]
        first_id_from_second_page = response_page_two.json()["data"][0]["id"]
        assert first_id_from_first_page != first_id_from_second_page

    @allure.feature("GET /user/id/comment")
    @allure.title("Get list of comment by user id")
    def test_get_comment_by_user_id(self, comment):
        response = comment.get_comment_by_user(user_id="60d0fe4f5311236168a109e2")
        response_validator(response=response, index_post_preview=0, model=Comment)
        response_validator(response=response, index_post_preview=-1, model=Comment)
        assert response.status_code == 200

    @allure.feature("GET /user/id/comment")
    @allure.title("Get list of comment by wrong user id Error")
    def test_get_comment_by_user_id_error(self, comment):
        response = comment.get_comment_by_user("test_id_123")
        assert response.status_code == 400
        assert response.json()["error"] == "PARAMS_NOT_VALID"

    @allure.feature("GET /post/id/comment")
    @allure.title("Get list of comment by post id")
    def test_get_comment_by_post_id(self, comment):
        response = comment.get_comment_by_post(post_id="60d21b5467d0d8992e610caf")
        response_validator(response=response, index_post_preview=0, model=Comment)
        response_validator(response=response, index_post_preview=-1, model=Comment)
        assert response.status_code == 200

    @allure.feature("GET /post/id/comment")
    @allure.title("Get list of comment by wrong post id Error")
    def test_get_comment_by_post_id_error(self, comment):
        response = comment.get_comment_by_user("test_id_123")
        assert response.status_code == 400
        assert response.json()["error"] == "PARAMS_NOT_VALID"

    @allure.feature("POST /comment/create")
    @pytest.mark.parametrize(
        "text",
        [
            pytest.param(
                "Test text",
                id="Test create comment valid text is str",
            ),
            pytest.param(
                123,
                id="Test create post valid only required text is int",
            ),
            pytest.param(
                False,
                id="Test create post valid only required text is boolean",
            ),
            pytest.param(
                None,
                id="Test create post valid only required text is null",
            ),
        ],
    )
    def test_create_comment(
        self, comment, create_and_after_delete_user, create_post_and_after_delete, text
    ):
        id_user = create_and_after_delete_user.json()["id"]
        id_post = create_post_and_after_delete.json()["id"]
        data = {"message": text, "owner": id_user, "post": id_post}
        response_create_comment = comment.create_comment(data=data)
        response_validator(response=response_create_comment, model=Comment)
        assert response_create_comment.status_code == 200

    @allure.feature("POST /comment/create")
    @pytest.mark.parametrize(
        "text, owner, post",
        [
            pytest.param(
                "Test text",
                "invalid id",
                "60d21b5467d0d8992e610caf",
                id="Test create comment invalid user id",
            ),
            pytest.param(
                "Test text",
                "60d0fe4f5311236168a109ca",
                "invalid id",
                id="Test create comment invalid post id",
            ),
            pytest.param(
                "Test text",
                None,
                "60d21b5467d0d8992e610caf",
                id="Test create comment invalid without user id",
            ),
            pytest.param(
                "Test text",
                "60d0fe4f5311236168a109ca",
                None,
                id="Test create comment invalid without post id",
            ),
        ],
    )
    def test_create_comment_invalid(self, comment, text, owner, post):
        data = {"message": text, "owner": owner, "post": post}
        response_create_comment = comment.create_comment(data=data)
        assert response_create_comment.status_code == 400
        assert response_create_comment.json()["error"] == "BODY_NOT_VALID"

    @allure.title("Delete comment")
    @allure.feature("DELETE /comment/comment_id")
    def test_delete_comment(self, comment, create_comment):
        id_comment = create_comment.json()["id"]
        response = comment.delete_comment(comment_id=id_comment)
        assert response.status_code == 200
