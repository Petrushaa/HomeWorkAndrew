from fastapi import FastAPI, HTTPException, Depends
from schemas.tasks import TaskCreate, TaskResponse
from api.auth import router as auth_router
from core.database import Base, engine
from core.dependency import get_current_user
from models.users import User
from models.tasks import Task
from repositories.tasks import TaskRepository

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.post("/tasks/", response_model=TaskResponse)
def taskPost(task: TaskCreate, current_user: User = Depends(get_current_user), task_repo: TaskRepository = Depends()):
    return task_repo.create(task_in=task, user_id=current_user.id)

@app.get("/tasks/", response_model=list[TaskResponse])
def taskGet(current_user: User = Depends(get_current_user), task_repo: TaskRepository = Depends()):
    return task_repo.get_all(user_id=current_user.id)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: User = Depends(get_current_user), task_repo: TaskRepository = Depends()):
    task = task_repo.get_by_id(task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskCreate, current_user: User = Depends(get_current_user), task_repo: TaskRepository = Depends()):
    task = task_repo.update(task_id=task_id, task_in=task_update, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), task_repo: TaskRepository = Depends()):
    success = task_repo.delete(task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}
