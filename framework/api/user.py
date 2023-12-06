import requests
import allure
from framework.api.base import Base


class User(Base):
    def __init__(self, config: dict):
        super().__init__(config)

    @allure.step("Make request to get list of users")
    def list_of_users(self, params: dict) -> requests.Response:
        endpoint = "user"
        response = self.make_get_request(endpoint=endpoint, params=params)
        return response

    @allure.step("Make request to get user by id")
    def get_user_by_id(self, id_user: str) -> requests.Response:
        endpoint = f"user/{id_user}"
        response = self.make_get_request(endpoint=endpoint)
        return response

    @allure.step("Make request to create user")
    def create_user(self, data: dict) -> requests.Response:
        endpoint = "user/create"
        response = self.make_post_request(endpoint=endpoint, data=data)
        return response

    @allure.step("Update user")
    def update_user(self, id_user: int, data: dict) -> requests.Response:
        endpoint = f"user/{id_user}"
        response = self.make_put_request(endpoint=endpoint, data=data)
        return response

    @allure.step("Delete user")
    def delete_user(self, id_user: int) -> requests.Response:
        endpoint = f"user/{id_user}"
        response = self.make_delete_request(endpoint=endpoint)
        return response
