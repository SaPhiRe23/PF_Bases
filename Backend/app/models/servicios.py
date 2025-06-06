from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ServicioEntrada(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    duracion: int = Field(..., gt=0)
    empresa_id: int = Field(..., gt=0)
    precio: float = Field(..., ge=0)
    descripcion: Optional[str] = Field(None, max_length=500)

class ServicioRespuesta(BaseModel):
    id: int
    nombre: str
    duracion: Optional[int]
    empresa_id: int
    precio: Optional[float]
    descripcion: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime