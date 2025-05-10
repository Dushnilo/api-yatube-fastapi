from pydantic import BaseModel
from datetime import datetime


class SCommentResponse(BaseModel):
    id: int
    author: str
    text: str
    created: datetime
    post: int | None

    class Config:
        from_attributes = True
