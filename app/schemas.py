
from pydantic import BaseModel, HttpUrl

class URLCreateDto(BaseModel):
    original: str

class URLResponseDto(BaseModel):
    original: HttpUrl
    short: str
    clicks: int

    class Config:
        orm_mode = True
