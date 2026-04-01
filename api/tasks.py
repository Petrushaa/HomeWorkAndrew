from fastapi import APIRouter, Depends, status, UploadFile, File
from dependency import get_current_user
from models import User
from schemas import TaskCreate, TaskResponse
from schemas import CommentCreate, CommentResponse
from services import TaskService
from services import CommentService

router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])

@router.post("/{task_id}/upload-avatar", response_model=TaskResponse)
async def upload_task_avatar(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.update_avatar(task_id=task_id, user_id=current_user.id, file=file)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.create_task(task_in=task, user_id=current_user.id)

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.get_all_tasks(user_id=current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.get_task_by_id(task_id=task_id, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.update_task(task_id=task_id, task_in=task_update, user_id=current_user.id)

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    await service.delete_task(task_id=task_id, user_id=current_user.id)
    return {"message": "Task deleted"}

@router.post(
    "/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    task_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(CommentService),
):
    return await service.create_comment(task_id=task_id, comment_in=comment, user_id=current_user.id)

@router.get("/{task_id}/comments", response_model=list[CommentResponse])
async def get_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(CommentService),
):
    return await service.get_comments_by_task(task_id=task_id, user_id=current_user.id)
