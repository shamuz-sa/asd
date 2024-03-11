from typing import List
import uuid

import _asyncio
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from models import Category, categories, Task
from tasks import tasks

router = APIRouter()


@router.post("/categories/")
async def create_category(category: Category):
    # Vérifier si la catégorie existe déjà
    if any(existing_category.name == category.name for existing_category in categories):
        raise HTTPException(status_code=422, detail=f"Une catégorie nommée '{category.name}' existe déjà.")

    # Attribuer un identifiant unique à la catégorie
    category.category_id = str(uuid.uuid4())
    category.tasks = []

    # Stocker la catégorie dans la liste des catégories
    categories.append(category)
    return category


def create_subcategory(parent_category: Category, subcategory_name: str):
    """
    Crée une nouvelle sous-catégorie et l'ajoute à la catégorie parente.
    Args:parent_category (Category): La catégorie parente à laquelle la sous-catégorie sera ajoutée.
        subcategory_name (str): Le nom de la sous-catégorie à créer.
    Returns:        Category: La sous-catégorie créée.
    Raises:        ValueError: Si une sous-catégorie avec le même nom existe déjà dans la catégorie parente.
    """
    # Vérifier si la sous-catégorie existe déjà
    if subcategory_name in parent_category.subcategories:
        raise ValueError(
            f"Une sous-catégorie nommée '{subcategory_name}' existe déjà dans la catégorie '{parent_category.name}'.")

    # Créer la nouvelle sous-catégorie
    new_subcategory = Category(name=subcategory_name, tasks=[], subcategories=[])

    # Ajouter la sous-catégorie à la liste des sous-catégories de la catégorie parente
    parent_category.subcategories.append(new_subcategory)

    return new_subcategory


@router.get("/categories/")
async def get_categories() -> list[Category]:
    return categories
