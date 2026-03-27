from fastapi import Depends, FastAPI, status

from api.auth import router as auth_router
from core.database import Base, engine
from core.dependency import get_current_user
from core.handlers import register_exception_handlers
from models.comments import Comment
from models.tasks import Task
from models.users import User
from schemas.comments import CommentCreate, CommentResponse
from schemas.tasks import TaskCreate, TaskResponse
from services.comments import CommentService
from services.tasks import TaskService

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
register_exception_handlers(app)


@app.post("/v1/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return service.create_task(task_in=task, user_id=current_user.id)


@app.get("/v1/tasks/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return service.get_all_tasks(user_id=current_user.id)


@app.get("/v1/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return service.get_task_by_id(task_id=task_id, user_id=current_user.id)


@app.put("/v1/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return service.update_task(task_id=task_id, task_in=task_update, user_id=current_user.id)


@app.delete("/v1/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    service.delete_task(task_id=task_id, user_id=current_user.id)
    return {"message": "Task deleted"}


@app.post(
    "/v1/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    task_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(CommentService),
):
    return service.create_comment(task_id=task_id, comment_in=comment, user_id=current_user.id)


@app.get("/v1/tasks/{task_id}/comments", response_model=list[CommentResponse])
def get_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(CommentService),
):
    return service.get_comments_by_task(task_id=task_id, user_id=current_user.id)
