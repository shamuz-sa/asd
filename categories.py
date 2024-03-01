from fastapi import APIRouter
from models import Category

router = APIRouter()

categories = {}


@router.post("/categories/")
async def create_category(category: Category):
    categories[category.name] = category.subcategories
    return category


@router.get("/categories/")
async def get_categories():
    return categories
