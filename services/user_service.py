from fastapi.responses import JSONResponse
import pymysql
from db.bd_mysql import get_db_connection
from models.user_model import User

class UserService:
    
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.con = get_db_connection()  # Obtiene la conexión directamente
        if self.con is None:
            raise Exception("No se pudo establecer conexión con la base de datos")
    
    async def get_users(self):
        """Consulta todos los usuarios y devuelve una respuesta estructurada."""
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM usuario")
                users = cursor.fetchall()

                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "message": "Usuarios obtenidos correctamente",
                        "data": users if users else []
                    }
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar usuarios: {str(e)}", "data": None}
            )
            
    async def get_user_by_id(self, user_id: int):
        """Consulta un usuario por su ID y devuelve una respuesta estructurada."""
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM usuario WHERE id = %s"
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()  # fetchone() devuelve un solo resultado

                if user:
                    return JSONResponse(
                        status_code=200,
                        content={
                            "success": True,
                            "message": "Usuario encontrado",
                            "data": user
                        }
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "success": False,
                            "message": "Usuario no encontrado",
                            "data": None
                        }
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"Error al consultar usuario: {str(e)}",
                    "data": None
                }
            )



    async def create_user(self, user_data: User):
        """Crea un nuevo usuario en la base de datos y devuelve una respuesta estructurada."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = "INSERT INTO usuario (nombre, apellido, numtelefono, password, estado) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_data.nombre, user_data.apellido, user_data.numtelefono, user_data.password, user_data.estado))
                self.con.commit()

                if cursor.lastrowid:
                    return JSONResponse(
                        status_code=201,
                        content={
                            "success": True,
                            "message": "Usuario creado exitosamente",
                            "data": {"user_id": cursor.lastrowid}
                        }
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"success": False, "message": "No se pudo crear el usuario", "data": None}
                    )
        except Exception as e:
            self.con.rollback()
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al crear usuario: {str(e)}", "data": None}
            )


    async def change_password(self, user_id: int, new_password: str) -> int:
        """Actualiza la contraseña de un usuario."""
        try:
            with self.con.cursor() as cursor:
                sql = "UPDATE usuario SET password=%s WHERE id=%s"
                cursor.execute(sql, (new_password, user_id))
                self.con.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al actualizar el password del usuario: {e}")
            self.con.rollback()
            return 0
        finally:
            self.close_connection()

    async def inactivate_user(self, user_id: int) -> int:
        """Inactiva un usuario cambiando su estado a 0."""
        try:
            with self.con.cursor() as cursor:
                sql = "UPDATE usuario SET estado=0 WHERE id=%s"
                cursor.execute(sql, (user_id,))
                self.con.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al inactivar el usuario: {e}")
            self.con.rollback()
            return 0
        finally:
            self.close_connection()

    def close_connection(self):
        """Llama al cierre de conexión de la base de datos."""
        self.db_instance.close_connection()
