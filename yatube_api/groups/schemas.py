from pydantic import BaseModel


class SGroupResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str

    class Config:
        from_attributes = True
