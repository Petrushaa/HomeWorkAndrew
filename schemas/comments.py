from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class CommentResponse(BaseModel):
    id: int
    text: str
    task_id: int
    owner_id: int

    class Config:
        from_attributes = True
