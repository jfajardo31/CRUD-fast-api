
from pydantic import BaseModel
from typing import Optional

# Modelo de usuario con validación de datos
class User(BaseModel):
    nombre: str
    apellido: str
    numtelefono: str
    correo: str
    password: str
    estado: Optional[int] = 1  # Estado por defecto activo (1)