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
            
            self.con.ping(reconnect=True) #pilas agregar esto para que no de lío la consulta al volverla a llamar
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
            print("Error en get_users:", str(e))  # <-- Esto te lo muestra en consola
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar usuarios: {str(e)}", "data": None}
            )

            
    async def get_user_by_id(self, user_id: int):
        """Consulta un usuario por su ID y devuelve una respuesta estructurada."""
        try:
            self.con.ping(reconnect=True)
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
        finally:
            self.close_connection()



    async def create_user(self, user_data: User):
        """Crea un nuevo usuario en la base de datos y devuelve una respuesta estructurada."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el correo ya existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
                cursor.execute(check_sql, (user_data.correo,))
                result = cursor.fetchone()
                
                if result[0] > 0:
                    return JSONResponse(
                        status_code=400,
                        content={"success": False, "message": "El correo ya ese encuenra registrado", "data": None}
                    )
                
                # Insertar el nuevo usuario
                sql = "INSERT INTO usuario (nombre, apellido, numtelefono, correo, password, estado) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_data.nombre, user_data.apellido, user_data.numtelefono, user_data.correo, user_data.password, user_data.estado))
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
        finally:
            self.close_connection()



    async def change_password(self, user_id: int, new_password: str):
        """Actualiza la contraseña de un usuario y retorna JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()
                
                if result[0] == 0: # Si NO existe el usuario
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)
                
                # Actualizar la contraseña
                sql = "UPDATE usuario SET password=%s WHERE id=%s"
                cursor.execute(sql, (new_password, user_id))
                self.con.commit() # Confirmar la transacción
                
                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Contraseña actualizada exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)
        except Exception as e:
            self.con.rollback() # Deshacer la transacción
            return JSONResponse(content={"success": False, "message": f"Error al actualizar la contraseña: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()




    async def inactivate_user(self, user_id: int):
        """Inactiva un usuario cambiando su estado a 0 y retorna JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()
                
                if result[0] == 0:  # Si el usuario no existe
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Inactivar usuario
                sql = "UPDATE usuario SET estado=0 WHERE id=%s"
                cursor.execute(sql, (user_id,))
                self.con.commit()  # Confirmar la transacción

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario inactivado exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=400)
        except Exception as e:
            self.con.rollback()  # Deshacer la transacción
            return JSONResponse(content={"success": False, "message": f"Error al inactivar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
            
            
    async def toggle_user_status(self, user_id: int):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Obtener estado actual
                get_estado_sql = "SELECT estado FROM usuario WHERE id=%s"
                cursor.execute(get_estado_sql, (user_id,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                estado_actual = result[0]
                nuevo_estado = 0 if estado_actual == 1 else 1

                update_sql = "UPDATE usuario SET estado=%s WHERE id=%s"
                cursor.execute(update_sql, (nuevo_estado, user_id))
                self.con.commit()

                return JSONResponse(content={"success": True, "message": "Estado actualizado correctamente."}, status_code=200)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al cambiar estado: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
    
    async def update_user(self, user_id: int, user_data: User):
        """
        Actualiza los datos de un usuario excepto el campo 'estado'.
        """
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Actualizar campos (excepto estado)
                update_sql = """
                    UPDATE usuario
                    SET nombre=%s, apellido=%s, numtelefono=%s, correo=%s, password=%s
                    WHERE id=%s
                """
                cursor.execute(update_sql, (
                    user_data.nombre,
                    user_data.apellido,
                    user_data.numtelefono,
                    user_data.correo,
                    user_data.password,
                    user_id
                ))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario actualizado correctamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)

        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()


    def close_connection(self):
        """Llama al cierre de conexión de la base de datos."""
        self.con.close()
