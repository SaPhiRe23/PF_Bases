from fastapi import FastAPI
from app.routers import usuarios
from fastapi.responses import RedirectResponse

app = FastAPI()

# Incluir los endpoints de usuarios
app.include_router(usuarios.router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
