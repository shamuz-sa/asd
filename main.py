from fastapi import FastAPI, APIRouter
from tasks import router as tasks_router
from categories import router as categories_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)


#Configuration CORS pour autoriser toutes les origines pendant le développement
origins = [
    "http://localhost",
    "http://localhost:4200",  # Ajoutez l'URL de votre application front-end
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Utilisez directement les instances d'APIRouter
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
