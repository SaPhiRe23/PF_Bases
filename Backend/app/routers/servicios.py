from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
import pyodbc
from app.database import get_connection
from app.models.servicios import ServicioEntrada, ServicioRespuesta

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.post("/", response_model=ServicioRespuesta)
def crear_servicio(servicio: ServicioEntrada):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Verificar que la empresa exista
        cursor.execute(
            "SELECT id FROM usuarios WHERE id = ? AND CAST(rol AS VARCHAR) = 'empresa'", 
            (servicio.empresa_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"Empresa con id {servicio.empresa_id} no existe"
            )

        # 2. Insertar el nuevo servicio
        cursor.execute("""
            INSERT INTO servicios (
                nombre,
                duracion,
                empresa_id,
                precio,
                descripcion,
                fecha_creacion,
                fecha_actualizacion
            )
            OUTPUT INSERTED.*  # Método más confiable que SCOPE_IDENTITY()
            VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
        """, (
            servicio.nombre,
            servicio.duracion,
            servicio.empresa_id,
            servicio.precio,
            servicio.descripcion
        ))
        
        # 3. Obtener el registro insertado directamente
        servicio_creado = cursor.fetchone()
        conn.commit()  # Confirmar después de obtener los datos

        if not servicio_creado:
            raise HTTPException(
                status_code=500,
                detail="No se pudo recuperar el servicio creado"
            )

        # 4. Mapear columnas a diccionario
        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, servicio_creado))

    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error de base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()


@router.get("/", response_model=List[ServicioRespuesta])
def obtener_servicios(empresa_id: Optional[int] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM servicios"
        params = []

        if empresa_id:
            query += " WHERE empresa_id = ?"
            params.append(empresa_id)

        cursor.execute(query, params)
        filas = cursor.fetchall()

        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.patch("/{id}", response_model=ServicioRespuesta)
def actualizar_servicio(id: int, servicio: ServicioEntrada):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM servicios WHERE id = ?", (id,))
        existente = cursor.fetchone()
        if not existente:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        cursor.execute("""
            UPDATE servicios SET 
                nombre = ?,
                duracion = ?,
                empresa_id = ?,
                precio = ?,
                descripcion = ?,
                fecha_actualizacion = GETDATE()
            WHERE id = ?
        """, (
            servicio.nombre,
            servicio.duracion,
            servicio.empresa_id,
            servicio.precio,
            servicio.descripcion,
            id
        ))
        conn.commit()

        cursor.execute("SELECT * FROM servicios WHERE id = ?", (id,))
        actualizado = cursor.fetchone()
        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, actualizado))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{id}")
def eliminar_servicio(id: int = Path(...)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si existe
        cursor.execute("SELECT id FROM servicios WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Eliminar
        cursor.execute("DELETE FROM servicios WHERE id = ?", (id,))
        conn.commit()
        return {"mensaje": "Servicio eliminado correctamente"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()