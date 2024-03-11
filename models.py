from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel

categories: List[Category] = []


class Task(BaseModel):
    task_id: str
    title: str
    description: str
    due_date: date
    priority: int
    category: str

    def __init__(self, task_id: int, title: str, description: str, due_date: date, priority: int, category: str):
        super().__init__(task_id=task_id, title=title, description=description, due_date=due_date, priority=priority,
                         category=category)
        verify_category(self, self.category, categories)

    def __lt__(self, other):
        """
        Méthode spéciale pour définir l'ordre de comparaison (<) entre les instances de Task.
        """
        return self.due_date < other.due_date


class Category(BaseModel):
    # categ_counter: int = 1
    category_id: int
    name: str
    tasks: List[Task]
    subcategories: List["Category"]

    def __init__(self, category_id: int, name: str, tasks: List[Task] = None, subcategories: List["Category"] = None):
        super().__init__(category_id=category_id, name=name, tasks=tasks or [],
                         subcategories=subcategories or [])
        # self.category_id = Category.categ_counter
        # Category.categ_counter += 1
        self.name = name
    # self.tasks: List[Task] = []
    # self.subcategories: List["Category"] = []


class CategoryTree:
    def __init__(self, category: Category, subcategories: List[Category] = None):
        self.category = category
        self.subcategories = subcategories

    def add_task(self, task: Task):
        self.category.tasks.append(task)

    def add_category(self, subcategory):
        if subcategory not in self.subcategories:
            self.subcategories.append(subcategory)

    def remove_category(self, subcategory):
        self.subcategories.remove(subcategory)

    def display_tree(self, category, niveau=0):
        category_toto = category or self.category
        ident = " " * niveau
        for subcategory in category_toto.subcategories:
            self.display_tree(subcategory, niveau + 1)

    def __str__(self, level=0):
        ret = "  " * level + str(self.category) + "\n"
        for child in self.subcategories:
            ret += child.__str__(level + 1)
        return ret


def verify_category(self, category_name: str, categories: List[Category]):
    """Verifie si la category existe dans la liste categories"""
    succes = [category for category in categories if category.name == category_name]
    if succes:
        category = succes[0]
        category.tasks.append(self)
    else:
        category_id = len(categories) + 1
        category = Category(category_id=category_id, name=category_name)
        category.tasks.append(self)
        categories.append(category)