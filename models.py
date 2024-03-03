from pydantic import BaseModel, Field
from typing import List
from datetime import date
import uuid


class Task(BaseModel):
    #task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: int
    title: str = Field(alias='titre')
    description: str
    due_date: date = Field(alias='date_limite')
    priority: int


class Category(BaseModel):
    category_id: int
    name: str
    tasks: List[Task] = []
    subcategories: List[str] = []
