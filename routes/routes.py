
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

@routes.post("/create-user/")
async def create_user(user:User):
    try:
        result = await user_service.create_user(user)
        return result
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return {"error": str(e)}
    
@routes.patch("/change-password/")
async def change_password(new_password:str,id:str):
    try:
        result= await user_service.change_password(new_password,id)
        return result
    except Exception as e:
        print(f"Error al cambiar el password del usuario: {e}")
        return {"error": str(e)}
    
@routes.patch("/inactivate/{id}")
async def inactivate_user(id:int):
    try:
        result= await user_service.inactivate_user(id)
        return result
    except Exception as e:
        print(f"Error al inactivar el usuario: {e}")
        return {"error": str(e)}      
    
@routes_b.get("/get-bolsillos/")
async def get_all_bolsillos():
    result=await bolsillo_service.get_bolsillos()
    return result

@routes_b.post("/create-bolsillo/")
async def create_bolsillo(bolsillo:Bolsillo):
    try:
        result = await bolsillo_service.create_bolsillo(bolsillo)
        return result
    except Exception as e:
        print(f"Error al crear el bolsillo: {e}")
        return {"error": str(e)}