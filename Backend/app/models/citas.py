from pydantic import BaseModel, Field
from datetime import datetime

class CitaEntrada(BaseModel):
    usuario_id: int = Field(..., gt=0)
    empleado_id: int = Field(..., gt=0)
    servicio_id: int = Field(..., gt=0)
    fecha_hora: datetime = Field(...)
