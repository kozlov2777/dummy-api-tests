from pydantic import BaseModel
from framework.responses.user_responses.user_preview import UserPreview


class Comment(BaseModel):
    id: str
    message: str
    owner: UserPreview
    post: str
    publishDate: str
