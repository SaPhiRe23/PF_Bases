from fastapi import APIRouter, Query
from typing import Optional
from app.database import get_connection
from app.models.usuarios import UsuarioEntrada
from fastapi import HTTPException
from app.models.usuarios import UsuarioEntrada


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def obtener_usuarios(
    id: Optional[int] = Query(None),
    nombre: Optional[str] = Query(None),
    email: Optional[str] = Query(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    # Construcción dinámica del query
    query = "SELECT id, nombre, email, telefono FROM usuarios"
    filtros = []
    valores = []

    if id is not None:
        filtros.append("id = ?")
        valores.append(id)

    if nombre is not None:
        filtros.append("nombre LIKE ?")
        valores.append(f"%{nombre}%")

    if email is not None:
        filtros.append("email LIKE ?")
        valores.append(f"%{email}%")

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    cursor.execute(query, valores)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"id": r[0], "nombre": r[1], "email": r[2], "telefono": r[3]} for r in rows]

@router.post("/")
def crear_usuario(usuario: UsuarioEntrada):
    if usuario.contrasena != usuario.confirmar_contrasena:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO usuarios (nombre, email, contrasena) VALUES (?, ?, ?)"
    values = (usuario.nombre, usuario.email, usuario.contrasena)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario creado correctamente"}