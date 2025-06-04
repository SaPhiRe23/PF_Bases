from fastapi import FastAPI
from app.routers import usuarios

app = FastAPI()

# Incluir los endpoints de usuarios
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de gestión de citas"}

