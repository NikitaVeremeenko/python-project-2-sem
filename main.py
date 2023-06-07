from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import date
from uuid import UUID, uuid4


app = FastAPI()


# Модель данных для задачи
class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    id: UUID
    title: str
    priority: PriorityEnum
    due_date: date
    completed: bool = False


# Хранилище данных в памяти
tasks_db = {}


# Маршруты API
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получение списка всех задач"""
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    """Получение задачи по идентификатору"""
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    """Создание новой задачи"""
    task.id = uuid4()
    tasks_db[task.id] = task
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, updated_task: Task):
    """Обновление задачи"""
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    updated_task.id = task.id
    tasks_db[task.id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: UUID):
    """Удаление задачи"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    del tasks_db[task_id]


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: UUID):
    """Отметка задачи как выполненной"""
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task.completed = True
    return task


@app.get("/tasks/sort/{sort_by}", response_model=List[Task])
def sort_tasks(sort_by: str):
    """Сортировка задач по приоритету или дате выполнения"""
    valid_sort_fields = ["priority", "due_date"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Некорректное поле сортировки. Доступные поля: {', '.join(valid_sort_fields)}",
        )
    return sorted(tasks_db.values(), key=lambda x: getattr(x, sort_by))


# Запуск сервера приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
