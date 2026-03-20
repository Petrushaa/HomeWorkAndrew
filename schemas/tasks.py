from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str
    completed: bool

class TaskResponse(TaskCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
