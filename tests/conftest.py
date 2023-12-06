import pytest

from framework.api.comment import Comment
from framework.api.user import User
from framework.api.post import Post
import os
import configparser


@pytest.fixture(scope="session")
def config():
    config_file_path = os.path.join("../config", "config.ini")
    config_parser = configparser.ConfigParser(os.environ)
    config_parser.read(config_file_path)

    api_config = {
        "base_url": config_parser.get("api", "base_url"),
        "token": config_parser.get("api", "token"),
    }

    yield api_config


@pytest.fixture
def user(config):
    user = User(config=config)
    yield user


@pytest.fixture
def post(config):
    post = Post(config=config)
    yield post


@pytest.fixture
def comment(config):
    comment = Comment(config=config)
    yield comment
