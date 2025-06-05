from fastapi import APIRouter, HTTPException
from datetime import date, time
from typing import Optional, List
from app.database import get_connection
from pydantic import BaseModel

router = APIRouter(prefix="/citas", tags=["Citas"])

# Modelo Pydantic para entrada de citas
class CitaEntrada(BaseModel):
    usuario_id: int
    servicio_id: int
    fecha: date
    hora: time
    duracion: Optional[int] = 30
    notas: Optional[str] = None

# Modelo para respuesta de citas
class CitaRespuesta(BaseModel):
    id: int
    usuario_id: int
    servicio_id: int
    fecha: date
    hora: time
    duracion: int
    estado: str
    notas: Optional[str]
    fecha_creacion: str
    fecha_actualizacion: str

@router.post("/", response_model=CitaRespuesta)
def crear_cita(cita: CitaEntrada):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (cita.usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si el servicio existe
        cursor.execute("SELECT id FROM servicios WHERE id = ?", (cita.servicio_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Insertar nueva cita
        cursor.execute("""
            INSERT INTO citas (
                usuario_id, 
                servicio_id, 
                fecha, 
                hora, 
                duracion, 
                notas
            ) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cita.usuario_id,
            cita.servicio_id,
            cita.fecha,
            cita.hora,
            cita.duracion,
            cita.notas
        ))
        conn.commit()

        # Obtener la cita recién creada
        cursor.execute("""
            SELECT * FROM citas 
            WHERE id = SCOPE_IDENTITY()
        """)
        cita_creada = cursor.fetchone()
        
        if not cita_creada:
            raise HTTPException(status_code=500, detail="Error al recuperar la cita creada")

        # Mapear resultado a diccionario
        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, cita_creada))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/", response_model=List[CitaRespuesta])
def obtener_citas(
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    estado: Optional[str] = None
):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT 
                c.id,
                c.usuario_id,
                c.servicio_id,
                c.fecha,
                c.hora,
                c.duracion,
                c.estado,
                c.notas,
                c.fecha_creacion,
                c.fecha_actualizacion,
                u.nombre as nombre_usuario,
                s.nombre as nombre_servicio
            FROM citas c
            JOIN usuarios u ON c.usuario_id = u.id
            JOIN servicios s ON c.servicio_id = s.id
            WHERE 1=1
        """
        params = []

        # Filtros opcionales
        if usuario_id:
            query += " AND c.usuario_id = ?"
            params.append(usuario_id)
        
        if fecha_inicio and fecha_fin:
            query += " AND c.fecha BETWEEN ? AND ?"
            params.extend([fecha_inicio, fecha_fin])
        elif fecha_inicio:
            query += " AND c.fecha >= ?"
            params.append(fecha_inicio)
        elif fecha_fin:
            query += " AND c.fecha <= ?"
            params.append(fecha_fin)
        
        if estado:
            query += " AND c.estado = ?"
            params.append(estado)

        query += " ORDER BY c.fecha, c.hora"

        cursor.execute(query, params)
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

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
