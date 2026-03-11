from fastapi import FastAPI, HTTPException
from models import TaskCreate
from schemas import Task

app = FastAPI()

tasks_db = []

@app.post("/tasks/")
def taskPost(task: TaskCreate):
    id = len(tasks_db)+1
    task1 = Task(id=id, title=task.title, description=task.description, completed=task.completed)    
    tasks_db.append(task1)
    return task1

@app.get("/tasks/")
def taskGet():
    return tasks_db

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task 
    
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskCreate):
    for task in tasks_db:
        if task.id == task_id:

            task.title = task_update.title
            task.description = task_update.description
            task.completed = task_update.completed
            return task
    
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            tasks_db.remove(task)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")