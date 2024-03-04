from typing import List

from fastapi import APIRouter
from models import Category, categories

router = APIRouter()


@router.post("/categories/")
async def create_category(category: Category):
    categories[category.name] = category.subcategories
    return category


@router.get("/categories/")
async def get_categories() -> list[Category]:
    return categories
