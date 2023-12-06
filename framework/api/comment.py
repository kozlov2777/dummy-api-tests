import allure
import requests

from framework.api.base import Base


class Comment(Base):
    def __init__(self, config: dict):
        super().__init__(config)

    @allure.step("Request to get list of comment")
    def get_list_of_comment(self, params: dict) -> requests.Response:
        endpoint = "comment"
        response = self.make_get_request(endpoint=endpoint, params=params)
        return response

    @allure.step("Request to get list of comment by post")
    def get_comment_by_post(self, post_id: str) -> requests.Response:
        endpoint = f"post/{post_id}/comment"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Request to get list of comment by user")
    def get_comment_by_user(self, user_id: str) -> requests.Response:
        endpoint = f"user/{user_id}/comment"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Request to create comment")
    def create_comment(self, data: dict) -> requests.Response:
        endpoint = f"comment/create"
        response = self.make_post_request(endpoint=endpoint, data=data)
        return response

    @allure.step("Request to delete comment")
    def delete_comment(self, comment_id) -> requests.Response:
        endpoint = f"comment/{comment_id}"
        response = self.make_delete_request(endpoint=endpoint)
        return response
