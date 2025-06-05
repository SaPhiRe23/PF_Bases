from pydantic import BaseModel, EmailStr, Field, model_validator

class UsuarioEntrada(BaseModel):
    nombre: str = Field(..., min_length=1)
    email: EmailStr = Field(...)
    contrasena: str = Field(..., min_length=6)
    confirmar_contrasena: str = Field(..., min_length=6)

    @model_validator(mode="after")
    def validar_contrasenas(cls, modelo):
        if modelo.contrasena != modelo.confirmar_contrasena:
            raise ValueError("Las contraseñas no coinciden")
        return modelo
