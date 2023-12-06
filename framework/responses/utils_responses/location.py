from pydantic import BaseModel, HttpUrl

class Location(BaseModel):
    street: str
    city: str
    state: str
    country: str
    timezone: str