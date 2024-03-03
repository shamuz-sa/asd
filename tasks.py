from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models import Task
from queue import LifoQueue, PriorityQueue

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
    global task_counter  # Utilisation de la variable globale task_counter

    # Attribution d'un identifiant unique à la tâche
    task.task_id = task_counter
    task_counter += 1
    tasks.append(task)  # Ajout de la tâche à la liste des tâches
    push_task_by_priority_stack(task)  # par priorite
    push_task_by_priority_queue(task)  # par date proche en priorité
    return task  # Retourne la tâche créée


def push_task_by_priority_queue(task: Task):
    priority_queue.put((task.due_date, task))


@router.get("/tasks/priority_queue", response_model=List[Task])
async def get_priority_queue():
    """
    Récupère les tâches organisées par date la plus proche
    """
    elements = []
    while not priority_queue.empty():
        elements.append(priority_queue.get()[1]) # pour add seulement l'objet task de la tuple

    # return list(priority_queue.queue)
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


@router.put("/up_tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    """ Mise à jour d'une tâche"""

    if 0 <= task_id < len(tasks):
        tasks[task_id] = updated_task
        return {"message": "Task updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    """ Mise à jour d'une tâche(meilleur version selon moi)"""
    # Find the task by ID
    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            # Update the task in place
            tasks[i] = updated_task
            return {"message": "Task updated successfully"}

    # Task not found
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/del_tasks/{task_id}")
async def delete_task(task_id: int):
    """
        Supprime une tâche par son ID.
    """
    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            deleted_task = tasks.pop(i)
            update_stack_queue() #mise à jour de la file et de la pile

            return {"message": "Task deleted successfully", "deleted_task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")
