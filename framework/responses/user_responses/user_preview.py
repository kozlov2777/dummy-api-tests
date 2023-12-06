from pydantic import BaseModel, HttpUrl


class UserPreview(BaseModel):
    id: str
    title: str
    firstName: str
    lastName: str
    picture: HttpUrl


