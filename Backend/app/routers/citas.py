from fastapi import APIRouter, HTTPException, Query, params
from datetime import date, time
from typing import Optional, List
from app.models.citas import CitaEntrada, CitaRespuesta
from app.database import get_connection

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("/", response_model=List[CitaRespuesta])
def obtener_citas(
    empresa_id: Optional[int] = Query(None),
    servicio_id: Optional[int] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    estado: Optional[str] = Query(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT 
                c.id,
                c.empresa_id,
                c.servicio_id,
                c.cliente_nombre,
                c.cliente_telefono,
                c.cliente_email,
                c.fecha,
                c.hora,
                c.duracion,
                c.estado,
                c.notas,
                c.fecha_creacion,
                c.fecha_actualizacion,
                s.nombre as nombre_servicio
            FROM citas c
            JOIN servicios s ON c.servicio_id = s.id
            WHERE 1=1
        """
        params = []

        if empresa_id is not None:
            query += " AND c.empresa_id = ?"
            params.append(empresa_id)
        if servicio_id is not None:
            query += " AND c.servicio_id = ?"
            params.append(servicio_id)
        if fecha_inicio is not None:
            query += " AND c.fecha >= ?"
            params.append(fecha_inicio)
        if fecha_fin is not None:
            query += " AND c.fecha <= ?"
            params.append(fecha_fin)
        if estado is not None:
            query += " AND c.estado = ?"
            params.append(estado)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        columnas = [col[0] for col in cursor.description]
        citas = [dict(zip(columnas, row)) for row in rows]

        return citas

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/", response_model=CitaRespuesta)
def crear_cita(cita: CitaEntrada):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO citas (
                empresa_id,
                servicio_id,
                cliente_nombre,
                cliente_telefono,
                cliente_email,
                fecha,
                hora,
                duracion,
                estado,
                notas,
                fecha_creacion,
                fecha_actualizacion
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
        """, (
            cita.empresa_id,
            cita.servicio_id,
            cita.cliente_nombre,
            cita.cliente_telefono,
            cita.cliente_email,
            cita.fecha,
            cita.hora,
            cita.duracion,
            cita.estado,
            cita.notas
        ))

        conn.commit()

        cursor.execute("SELECT * FROM citas WHERE id = SCOPE_IDENTITY()")
        cita_creada = cursor.fetchone()

        if not cita_creada:
            raise HTTPException(status_code=500, detail="Error al recuperar la cita creada")

        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, cita_creada))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


def obtener_citas(
    empresa_id: Optional[int] = None,
    servicio_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    estado: Optional[str] = None
):
    ...
    query = """
        SELECT 
            c.id,
            c.empresa_id,
            c.servicio_id,
            c.cliente_nombre,
            c.cliente_telefono,
            c.cliente_email,
            c.fecha,
            c.hora,
            c.duracion,
            c.estado,
            c.notas,
            c.fecha_creacion,
            c.fecha_actualizacion,
            s.nombre as nombre_servicio
        FROM citas c
        JOIN servicios s ON c.servicio_id = s.id
        WHERE 1=1
    """
    ...
    if empresa_id:
        query += " AND c.empresa_id = ?"
        params.append(empresa_id)
    ...


@router.delete("/{id}")
def eliminar_cita(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si la cita existe
        cursor.execute("SELECT id FROM citas WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        # Eliminar la cita
        cursor.execute("DELETE FROM citas WHERE id = ?", (id,))
        conn.commit()
        
        return {"mensaje": "Cita eliminada exitosamente"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.patch("/{id}/estado")
def actualizar_estado_cita(id: int, estado: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Validar estado
        estados_validos = ['pendiente', 'confirmada', 'cancelada', 'completada']
        if estado not in estados_validos:
            raise HTTPException(
                status_code=400, 
                detail=f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )

        # Actualizar estado
        cursor.execute("""
            UPDATE citas 
            SET estado = ?, 
                fecha_actualizacion = GETDATE()
            WHERE id = ?
        """, (estado, id))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        return {"mensaje": "Estado de cita actualizado exitosamente"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
