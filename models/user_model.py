
from pydantic import BaseModel

class User(BaseModel):
    nombre:str
    apellido:str
    numtelefono:str
    password:str
    estado:int
    
