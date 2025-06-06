from fastapi import FastAPI
from app.routers import servicios
from app.routers import usuarios
from fastapi.responses import RedirectResponse
from app.routers import citas
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Cambia según tu puerto Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los endpoints de usuarios
app.include_router(usuarios.router)
app.include_router(citas.router)
app.include_router(servicios.router)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
