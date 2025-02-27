from models.user_model import User
from pydantic import BaseModel
from typing import Union

class Bolsillo(BaseModel):
    nombre:str
    saldo:int
    usuario: Union[int, User]