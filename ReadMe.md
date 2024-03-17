# Projet de fin de semestre pour le cours de : Algorithme et Structure de Donnée
## Objectif : 
    L'objectif de ce projet est de créer un système de gestion de tâches où les utilisateurs peuvent organiser leurs tâches quotidiennes. 
    Le programme doit permettre l'ajout, la suppression, la mise à jour et la visualisation des tâches. 
    De plus, le projet doit inclure une interface graphique moderne pour une meilleure expérience utilisateur.

## Outils :
    - FastApi: il s'agit d'un framework web morderne pour la creation d'API Restful en python
    - Angular: il s'agit d'un framework Javascript permettant la creation d'application web et particulierement 
        les SPA(Single Page Application: applications web accessibles via une page web unique qui permet de fluidifier 
        l’expérience utilisateur et d’éviter les chargements de pages à chaque nouvelle action)

## Pré-requis:
    - python version 3.12 
    - fastApi : pip install fastapi
    - uvicorn : pip install "uvicorn[standard]"

## Pour lancer le projet : 
    -uvicorn main:app --reload

## Explication des fichiers:
    main.py: il s'agit du point d'entrée de l'api
    models.py: c'est là que nous avions mis toutes nos classes
    tasks.py: c'est là que nous avions mis tous les traitements concernant les taches
    categories.py: c'est là que nous avions mis tous les traitements concernant les categories
