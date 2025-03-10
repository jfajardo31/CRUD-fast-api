
from fastapi import APIRouter
from services.user_service import UserService
from services.bolsillo_service import BolsilloService
from models.bolsillo_model import Bolsillo
from models.user_model import User

routes=APIRouter(prefix="/user", tags=["User"])
routes_b=APIRouter(prefix="/bolsillo", tags=["Bolsillo"])

user_service = UserService()
user_model=User
bolsillo_service=BolsilloService()
bolsillo_model=Bolsillo

@routes.get("/get-users/")
async def get_all_users():
    result=await user_service.get_users()
    return result

@routes.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user_by_id(user_id)

#Modelo para crear rutas, crear una para cada método
@routes.post("/nombre-metodo/") 
async def nombre_metodo():
    return "Nombre método"
   
@routes.post("/create-user/")
async def create_user(user: User):
    return await user_service.create_user(user)

@routes.patch("/change-password/")
async def change_password(id: str, new_password: str):
    return await user_service.change_password(id, new_password)

@routes.patch("/inactivate/{id}")
async def inactivate_user(id: int):
    return await user_service.inactivate_user(id)

@routes_b.get("/get-bolsillos/")
async def get_all_bolsillos():
    return await bolsillo_service.get_bolsillos()

@routes_b.get("/get-bolsillo/{id_bolsillo}")
async def get_bolsillo(id_bolsillo: int):
    return await bolsillo_service.get_bolsillo(id_bolsillo)

@routes_b.post("/create-bolsillo/")
async def create_bolsillo(bolsillo: Bolsillo):
    return await bolsillo_service.create_bolsillo(bolsillo)