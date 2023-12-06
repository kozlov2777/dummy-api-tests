import requests
import logging
from utils.logger import log_response


class Base:
    def __init__(self, config: dict):
        self.base_url = config.get("base_url")
        self.token = config.get("token")
        self.headers = {"Content-Type": "application/json", "app-id": f"{self.token}"}

    def get_session(self) -> requests.Session:
        session = requests.Session()
        session.headers = self.headers
        return session

    def make_get_request(self, endpoint: str, params=None) -> requests.Response:
        session = self.get_session()
        try:
            response = session.get(url=f"{self.base_url}{endpoint}", params=params)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise err
        except Exception as err:
            logging.error(err)
            raise err
        log_response(response)
        return response

    def make_post_request(self, endpoint: str, data: dict) -> requests.Response:
        session = self.get_session()
        try:
            response = session.post(url=f"{self.base_url}{endpoint}", json=data)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise err
        except Exception as err:
            logging.error(err)
            raise err
        log_response(response)
        return response

    def make_put_request(self, endpoint: str, data: dict) -> requests.Response:
        session = self.get_session()
        try:
            response = session.put(url=f"{self.base_url}{endpoint}", json=data)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise err
        except Exception as err:
            logging.error(err)
            raise err
        log_response(response)
        return response

    def make_delete_request(self, endpoint: str) -> requests.Response:
        session = self.get_session()
        try:
            response = session.delete(url=f"{self.base_url}{endpoint}")
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise err
        except Exception as err:
            logging.error(err)
            raise err
        log_response(response)
        return response
