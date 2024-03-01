from typing import List, Optional

from fastapi import APIRouter, HTTPException

from models import Task

router = APIRouter()

tasks: List[Task] = []  # declaration de la liste des taches
priority_stack: List[Task] = []  # declaration de la liste des tache par priorité
task_counter = 1  # Utilisé pour attribuer des identifiants uniques aux tâches


@router.post("/add_tasks/")
async def create_task(task: Task):
    global task_counter  # Utilisation de la variable globale task_counter

    # Attribution d'un identifiant unique à la tâche
    task.task_id = task_counter
    task_counter += 1
    tasks.append(task)  # Ajout de la tâche à la liste des tâches
    push_task_by_priority(task)
    return task  # Retourne la tâche créée


def push_task_by_priority(task: Task):
    """
    add une tâche à la pile en function de sa priority.
    """
    priority_stack.append(task)
    priority_stack.sort(key=lambda x: x.priority, reverse=False)  # reverse false: ordre croissant


@router.get("/tasks/priority", response_model=List[Task])
async def get_priority_tasks():
    """
    Récupère les tâches organisées par ordre de priorité.
    """
    return priority_stack


def remove_task_from_priority_stack(task: Task):
    """
    Supprime une tâche de la pile en fonction de sa priorité.
    """
    priority_stack.remove(task)
    priority_stack.sort(key=lambda x: x.priority, reverse=True)


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
    print(tasks)
    return tasks


@router.put("/up_tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    if 0 <= task_id < len(tasks):
        tasks[task_id] = updated_task
        return {"message": "Task updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
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

            return {"message": "Task deleted successfully", "deleted_task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")
