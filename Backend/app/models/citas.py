from pydantic import BaseModel, Field, validator
from datetime import date, time, datetime
from typing import Optional

class CitaEntrada(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    servicio: str = Field(..., description="Nombre o ID del servicio")
    fecha: str = Field(..., description="Fecha en formato DD-MM-YYYY")
    hora: str = Field(..., description="Hora en formato HH:MM AM/PM (ej. 02:30 PM)")
    notas: Optional[str] = Field(default=None, max_length=500, description="Notas adicionales")

    @validator('fecha')
    def validar_fecha(cls, v):
        try:
            day, month, year = map(int, v.split('-'))
            return date(year, month, day)  # Convierte a objeto date
        except:
            raise ValueError("Formato de fecha inválido. Use DD-MM-YYYY")

    @validator('hora')
    def validar_hora(cls, v):
        try:
            from datetime import datetime
            return datetime.strptime(v, "%I:%M %p").time()  # Convierte a objeto time
        except:
            raise ValueError("Formato de hora inválido. Use HH:MM AM/PM (ej. 09:00 AM)")

class CitaRespuesta(CitaEntrada):
    id: int
    estado: str = Field(
        default="pendiente",
        description="Estado de la cita: pendiente|confirmada|cancelada|completada"
    )
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            time: lambda v: v.strftime('%H:%M:%S'),
            datetime: lambda v: v.isoformat()
        }