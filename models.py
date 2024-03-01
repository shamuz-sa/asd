from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Task(BaseModel):
    task_id: int
    title: str = Field(alias='titre')
    description: str
    due_date: date = Field(alias='date_limite')
    priority: int


class Category(BaseModel):
    name: str
    subcategories: List[str] = []
