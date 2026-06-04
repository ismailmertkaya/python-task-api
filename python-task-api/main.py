"""
Task Manager REST API — built with FastAPI
A clean, modern REST API with automatic documentation.

Run: uvicorn main:app --reload
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Task Manager API",
    description="A simple REST API to manage tasks. Built with FastAPI + Pydantic.",
    version="1.0.0",
)



class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500)
    priority: int = Field(default=1, ge=1, le=3, description="1=Low, 2=Medium, 3=High")

class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=3)
    completed: Optional[bool] = None

class Task(BaseModel):
    """Full task schema returned by the API."""
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    created_at: str
    updated_at: Optional[str]



tasks: dict[int, dict] = {}
next_id = 1

def priority_label(p: int) -> str:
    return {1: "Low", 2: "Medium", 3: "High"}.get(p, "Unknown")



@app.get("/", tags=["Root"])
def root():
    return {"message": "Task Manager API is running!", "docs": "/docs"}


@app.get("/tasks", response_model=list[Task], tags=["Tasks"])
def get_all_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[int] = Query(None, ge=1, le=3, description="Filter by priority level"),
):
    """Get all tasks, with optional filters."""
    result = list(tasks.values())

    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]

    return result


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    """Get a single task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks[task_id]


@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Create a new task."""
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    }
    tasks[next_id] = new_task
    next_id += 1
    return new_task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, updates: TaskUpdate):
    """Partially update a task (only provide fields you want to change)."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task = tasks[task_id]
    update_data = updates.model_dump(exclude_unset=True)  # only changed fields

    for field, value in update_data.items():
        task[field] = value

    task["updated_at"] = datetime.now().isoformat()
    return task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    del tasks[task_id]


@app.get("/tasks/stats/summary", tags=["Stats"])
def get_stats():
    """Get summary statistics about tasks."""
    all_tasks = list(tasks.values())
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t["completed"])
    return {
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "by_priority": {
            "high": sum(1 for t in all_tasks if t["priority"] == 3),
            "medium": sum(1 for t in all_tasks if t["priority"] == 2),
            "low": sum(1 for t in all_tasks if t["priority"] == 1),
        }
    }
