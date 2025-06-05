from fastapi import APIRouter
from app.models.citas import CitaEntrada
from app.database import get_connection

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("/")
def crear_cita(cita: CitaEntrada):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO citas (usuario_id, empleado_id, servicio_id, fecha_hora) VALUES (?, ?, ?, ?)",
        (cita.usuario_id, cita.empleado_id, cita.servicio_id, cita.fecha_hora)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Cita registrada exitosamente"}

