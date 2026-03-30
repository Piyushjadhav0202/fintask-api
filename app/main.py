from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks: List[Task] = [
    Task(id=1, title="Learn CI/CD", done=False),
    Task(id=2, title="Build FastAPI app", done=False)
]

next_id = 3

@app.get("/")
def root():
    return {"app": "FinTask API", "status": "running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime": time.time()
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, updated: Task):
    for t in tasks:
        if t.id == task_id:
            t.title = updated.title
            t.done = updated.done
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
