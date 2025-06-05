from fastapi import APIRouter, Query
from typing import Optional
from app.database import get_connection
from app.models.usuarios import CredencialesUsuario, UsuarioAutenticado, UsuarioEntrada
from fastapi import HTTPException
from app.models.usuarios import UsuarioEntrada


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/login", response_model=UsuarioAutenticado)
def login_usuario(credenciales: CredencialesUsuario):
    conn = get_connection()
    cursor = conn.cursor()

    # Buscar usuario por email
    query = "SELECT id, nombre, email, contrasena, rol FROM usuarios WHERE email = ?"
    cursor.execute(query, (credenciales.email,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    id, nombre, email, contrasena_bd, rol = row

    if credenciales.contrasena != contrasena_bd:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return UsuarioAutenticado(id=id, nombre=nombre, email=email, rol=rol)

from fastapi import Path

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int = Path(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario eliminado"}


@router.get("/")
def obtener_usuarios(
    id: Optional[int] = Query(None),
    nombre: Optional[str] = Query(None),
    email: Optional[str] = Query(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, nombre, email, telefono, contrasena FROM usuarios"
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

    return [{
        "id": r[0],
        "nombre": r[1],
        "email": r[2],
        "contrasena": r[4]
    } for r in rows]


@router.post("/")
def crear_usuario(usuario: UsuarioEntrada):
    if usuario.contrasena != usuario.confirmar_contrasena:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)"
    values = (usuario.nombre, usuario.email, usuario.contrasena, usuario.rol)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario creado correctamente"}
