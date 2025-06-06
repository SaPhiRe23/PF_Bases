from pydantic import BaseModel, Field, validator
from datetime import date, time, datetime
from typing import Optional

class CitaEntrada(BaseModel):
    empresa_id: int
    servicio_id: int
    cliente_nombre: str
    cliente_telefono: Optional[str] = None
    cliente_email: Optional[str] = None
    fecha: date
    hora: time
    duracion: Optional[int] = 30
    estado: Optional[str] = "pendiente"
    notas: Optional[str] = None


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

# Modelo para respuesta de citas
class CitaRespuesta(BaseModel):
    id: int
    nombre: str
    fecha: date
    hora: time
    duracion: int
    estado: str
    notas: Optional[str]
    fecha_creacion: str
    fecha_actualizacion: str