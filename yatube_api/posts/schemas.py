from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SPostRequest(BaseModel):
    text: str = Field(...)
    image: Optional[str] = Field(None)
    group: Optional[int] = Field(None)


class SPostResponse(BaseModel):
    id: int
    author: str
    text: str
    pub_date: datetime
    image: str | None
    group: int | None


class SPostsResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[SPostResponse]
