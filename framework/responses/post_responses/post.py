from pydantic import BaseModel, HttpUrl
from typing import List
from framework.responses.user_responses.user_preview import UserPreview


class Post(BaseModel):
    id: str
    text: str
    image: HttpUrl
    likes: int = 0
    link: HttpUrl
    tags: List[str]
    publishDate: str
    owner: UserPreview