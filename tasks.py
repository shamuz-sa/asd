import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models import Task
from queue import LifoQueue, PriorityQueue, SimpleQueue

router = APIRouter()

tasks: List[Task] = []  # declaration de la liste des taches
priority_stack: LifoQueue[Task] = LifoQueue()  # declaration de la pile des taches par priorité
task_counter = 1  # Utilisé pour attribuer des identifiants uniques aux tâches
priority_queue = PriorityQueue()  # declaration de la file des taches par date en priorité


@router.post("/add_tasks/")
async def create_task(task: Task):
    """
    Creation d'une nouvelle tache
    """
    # global task_counter  # Utilisation de la variable globale task_counter

    # Attribution d'un identifiant unique à la tâche
    # task.task_id = task_counter
    # task_counter += 1
    task.task_id = str(uuid.uuid4())
    tasks.append(task)  # Ajout de la tâche à la liste des tâches
    push_task_by_priority_stack(task)  # par priorite
    push_task_by_priority_queue(task)  # par date proche en priorité
    return task  # Retourne la tâche créée


def push_task_by_priority_queue(task: Task):
    try:
        priority_queue.put((task.due_date, task))
    except Exception as e:
        print(f"Erreur lors de l'ajout à la file de priorité : {e}")

    # print(type(task.due_date))
    # print("la taille de la queue", priority_queue.qsize())


@router.get("/tasks/priority_queue", response_model=List[Task])
async def get_priority_queue():
    """
    Récupère les tâches organisées par date la plus proche
    """
    # Crée une liste pour stocker temporairement les tâches
    elements = []

    # Crée une copie temporaire de la file de priorité sans retirer les éléments
    temp_queue = PriorityQueue()

    # Parcours la file de priorité principale
    while not priority_queue.empty():
        # Récupère la date de fin et la tâche de la file de priorité principale
        _, task = priority_queue.get()

        # Ajoute la tâche à la copie temporaire et à la liste
        temp_queue.put((task.due_date, task))
        elements.append(task)

    # Restaure la file de priorité principale avec les éléments copiés
    while not temp_queue.empty():
        # Récupère la date de fin et la tâche de la copie temporaire
        _, task = temp_queue.get()

        # Réinsère la tâche dans la file de priorité principale
        priority_queue.put((task.due_date, task))

    # Affiche les éléments sans les retirer de la file
    print(f"Les éléments de la file sont : {elements}")

    # Retourne la liste des tâches
    return elements


def push_task_by_priority_stack(task: Task):
    """
    Ajouter un task à la pile par ordre croissant de priority 0 1 2 3
    """
    priority_stack.put(task)  # Utilisation de put() pour ajouter à la pile
    priority_stack.queue.sort(key=lambda x: x.priority, reverse=True)  # reverse = True par ordre decroissant


def update_stack_queue():
    """Mise a jour d'une pile apres modification
     sur une tache dans la liste des taches"""
    priority_stack.queue.clear()  # vider la pile et la reremplir ensuite
    for task in tasks:
        push_task_by_priority_stack(task)

    # vider la file et la reremplir ensuite
    priority_queue.queue.clear()
    for task in tasks:
        push_task_by_priority_queue(task)


@router.get("/tasks/priority", response_model=List[Task])
async def get_priority_tasks():
    """
    Récupère les tâches organisées par ordre de priorité.
    """
    return list(priority_stack.queue)


def remove_task_from_priority_stack(task: Task, stack: List[Task]):
    """
    Supprime une tâche de la pile en fonction de sa priorité.
    """
    if task in priority_stack:
        stack.remove(task)
        stack.sort(key=lambda x: x.priority, reverse=True)


def find_task_index(task_id: int) -> Optional[int]:
    """
    Recherche l'index d'une tâche par son ID.
    Retourne None si la tâche n'est pas trouvée.
    """
    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            return i

    return None


@router.get("/get_tasks/")
async def get_tasks():
    """ Recuperer la liste des tasks"""
    print(tasks)
    return tasks


@router.put("/tasks/{task_id}")
async def update_task(task_id: str, updated_task: Task):
    """ Mise à jour d'une tâche"""
    task_dict = updated_task.dict()
    matching_task = [task for task in tasks if task.task_id == task_id]
    if matching_task:
        task = matching_task[0]
     #   task.task_id = task_dict["task_id"]
        task.title = task_dict["title"]
        task.description = task_dict["description"]
        task.due_date = task_dict["due_date"]
        task.priority = task_dict["priority"]
        return {"message": "Task updated successfully"}
    else:
        print(f"Task with {task_id}not found")


@router.delete("/del_tasks/{task_id}")
async def delete_task(task_id: int):
    """
        Supprime une tâche par son ID.
    """
    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            deleted_task = tasks.pop(i)
            update_stack_queue()  # mise à jour de la file et de la pile

            return {"message": "Task deleted successfully", "deleted_task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")
