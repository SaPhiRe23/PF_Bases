from pydantic import BaseModel, Field
from datetime import datetime

class CitaEntrada(BaseModel):
    usuario_id: int = Field(..., gt=0, description="ID del usuario que agenda la cita")
    empleado_id: int = Field(..., gt=0, description="ID del empleado que atiende la cita")
    servicio_id: int = Field(..., gt=0, description="ID del servicio solicitado")
    fecha_hora: datetime = Field(..., description="Fecha y hora de la cita")
