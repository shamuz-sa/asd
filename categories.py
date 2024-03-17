from typing import List
import uuid

from fastapi import APIRouter, HTTPException

from models import Category

router = APIRouter()

# Assuming categories is a list where you store your categories
list_category: List[Category] = []


@router.post("/categories/")
async def create_category(category: Category):
    """Creation d'une nouvelle categorie"""
    # Vérifier si la catégorie existe déjà
    if any(existing_category.name == category.name for existing_category in list_category):
        raise HTTPException(status_code=422, detail=f"Une catégorie nommée '{category.name}' existe déjà.")

    # Attribuer un identifiant unique à la catégorie
    category.category_id = str(uuid.uuid4())
    category.tasks = []

    # Stocker la catégorie dans la liste des catégories
    list_category.append(category)
    return category


@router.put("/categories/{name}", response_model=Category)
async def update_category(name: str, category: Category):
    """Mise a jour d'une categorie"""
    for index, stored_category in enumerate(list_category):
        if stored_category.name == name:
            # Conserver l'identifiant de la catégorie
            category.category_id = stored_category.category_id
            list_category[index] = category
            return category
    raise HTTPException(status_code=404, detail="La catégorie spécifiée n'a pas été trouvée.")


@router.delete("/categories/{name}")
async def delete_category(name: str):
    """Suppression d'une categorie"""
    for index, stored_category in enumerate(list_category):
        if stored_category.name == name:
            del list_category[index]
            return {"message": "Catégorie supprimée avec succès"}
    raise HTTPException(status_code=404, detail="La catégorie spécifiée n'a pas été trouvée.")


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
    return list_category
