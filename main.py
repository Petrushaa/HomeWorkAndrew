import uuid
import sys
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from core.database import Base, engine, get_db
from core.dependency import get_current_user
from core.handlers import register_exception_handlers
from core.config import VERSION, ENV
from models.comments import Comment
from models.tasks import Task
from models.users import User
from schemas.comments import CommentCreate, CommentResponse
from schemas.tasks import TaskCreate, TaskResponse
from services.comments import CommentService
from services.tasks import TaskService
from services.storage import StorageService
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
register_exception_handlers(app)


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
        
    storage = StorageService()
    minio_ok = await storage.check_connection()
    minio_status = "ok" if minio_ok else "error"
    
    status_code = status.HTTP_200_OK if db_status == "ok" and minio_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ok" if status_code == 200 else "error", "db": db_status, "minio": minio_status}

@app.get("/info")
async def info():
    return {
        "version": VERSION,
        "environment": ENV,
        "python_version": sys.version
    }


@app.post("/v1/tasks/{task_id}/upload-avatar", response_model=TaskResponse)
async def upload_task_avatar(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    storage = StorageService()
    
    # Read file
    content = await file.read()
    ext = file.filename.split('.')[-1] if file.filename else "bin"
    key = f"tasks/{task_id}_{uuid.uuid4()}.{ext}"
    
    # Upload to MinIO
    try:
        url = await storage.upload_file(content, key, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
    # Update Task in DB
    task = await service.update_avatar(task_id=task_id, user_id=current_user.id, avatar_url=url)
    return task


@app.post("/v1/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.create_task(task_in=task, user_id=current_user.id)


@app.get("/v1/tasks/", response_model=list[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.get_all_tasks(user_id=current_user.id)


@app.get("/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.get_task_by_id(task_id=task_id, user_id=current_user.id)


@app.put("/v1/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    return await service.update_task(task_id=task_id, task_in=task_update, user_id=current_user.id)


@app.delete("/v1/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    await service.delete_task(task_id=task_id, user_id=current_user.id)
    return {"message": "Task deleted"}


@app.post(
    "/v1/tasks/{task_id}/comments",
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


@app.get("/v1/tasks/{task_id}/comments", response_model=list[CommentResponse])
async def get_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(CommentService),
):
    return await service.get_comments_by_task(task_id=task_id, user_id=current_user.id)
