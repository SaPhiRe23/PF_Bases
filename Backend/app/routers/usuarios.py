from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, telefono FROM usuarios")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "email": r[2], "telefono": r[3]} for r in rows]

