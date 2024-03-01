from pydantic import BaseModel
from typing import List
from datetime import date


class Task(BaseModel):
    task_id: int
    title: str
    description: str
    due_date: date
    priority: int


class Category(BaseModel):
    name: str
    subcategories: List[str] = []
