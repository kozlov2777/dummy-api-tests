from typing import Optional
from pydantic import BaseModel, HttpUrl
from framework.responses.utils_responses.location import Location


class UserFull(BaseModel):
    id: str
    title: str
    firstName: str
    lastName: str
    gender: Optional[str]
    email: str
    dateOfBirth: str
    registerDate: str
    phone: str
    picture: HttpUrl
    location: Optional[Location]
