import requests
import allure
from framework.api.base import Base


class Post(Base):
    def __init__(self, config: dict):
        super().__init__(config)

    @allure.step("Request to get list of post")
    def get_list_of_posts(self, params: dict) -> requests.Response:
        endpoint = "post"
        response = self.make_get_request(endpoint=endpoint, params=params)
        return response

    @allure.step("Request to get list of post by user")
    def get_post_by_user_id(self, user_id: str) -> requests.Response:
        endpoint = f"user/{user_id}/post"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Request to get list of post by tag")
    def get_list_of_post_by_tag(self, tag_id: str) -> requests.Response:
        endpoint = f"tag/{tag_id}/post"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Request to get list of post by post_id")
    def get_post_by_id(self, id_post: str) -> requests.Response:
        endpoint = f"post/{id_post}"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Request to create post")
    def create_post(self, data: dict) -> requests.Response:
        endpoint = f"post/create"
        response = self.make_post_request(endpoint=endpoint, data=data)
        return response

    @allure.step("Request to update post")
    def update_post(self, post_id: str, data: dict) -> requests.Response:
        endpoint = f"post/{post_id}"
        response = self.make_put_request(endpoint=endpoint, data=data)
        return response

    @allure.step("Request to update post")
    def delete_post(self, post_id: str) -> requests.Response:
        endpoint = f"post/{post_id}"
        response = self.make_delete_request(endpoint=endpoint)
        return response
