from pydantic import BaseModel, HttpUrl
from typing import List
from framework.responses.user_responses.user_preview import UserPreview


class PostPreview(BaseModel):
    id: str
    text: str
    image: HttpUrl | str
    likes: int = 0
    tags: List[str]
    publishDate: str
    owner: UserPreview
