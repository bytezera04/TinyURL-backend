
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreateDto(BaseModel):
    original: str

class URLResponseDto(BaseModel):
    original: HttpUrl
    short: str
    clicks: int
    created_at: datetime
    last_clicked_at: Optional[datetime] = None

    class Config:
        orm_mode = True
