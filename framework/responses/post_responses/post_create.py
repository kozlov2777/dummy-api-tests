from pydantic import BaseModel


class Location(BaseModel):
    street: str
    city: str
    state: str
    country: str
    timezone: str
