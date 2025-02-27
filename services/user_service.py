from db.bd_mysql import get_db_connection

class UserService:
    
    def __init__(self):
        # Inicializa la conexión al crear una instancia de la clase
        self.con = get_db_connection()
    
    # Función para consultar usuarios 
    async def get_users(self):
        
        try:
            with self.con.cursor() as cursor:
                sql = "SELECT * FROM usuario"
                cursor.execute(sql)
                users = cursor.fetchall()  # fetchall para obtener todos los registros
                return users
        except Exception as e:
            print(f"Error al consultar usuarios: {e}")
            return None

    # Función para crear usuarios
    async def create_user(self, user_data):
        try:
            with self.con.cursor() as cursor:
                sql = "INSERT INTO usuario (nombre, apellido,numtelefono,password,estado) VALUES (%s, %s,%s,%s,%s)"
                cursor.execute(sql, (user_data.nombre, user_data.apellido, user_data.numtelefono,user_data.password,1))
                self.con.commit()                                                                 
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            self.con.rollback()
            return None

    async def change_password(self, new_password,id):
        try:
            with self.con.cursor() as cursor:
                sql="UPDATE usuario SET password=%s WHERE id=%s"
                cursor.execute(sql,(new_password,id))
                self.con.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al actualizar erl password del usuario: {e}")
            self.con.rollback()
            return None
        
    async def inactivate_user(self,id):
        try:
            with self.con.cursor() as cursor:
                sql="UPDATE usuario SET estado=0 WHERE id=%s"
                cursor.execute(sql,(id))
                self.con.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al inactivar el password del usuario: {e}")
            self.con.rollback()
            return None
                
    async def update_user_password(self, user_id, new_password):
        try:
            with self.con.cursor() as cursor:
                sql = "UPDATE usuario SET password=%s WHERE id=%s"
                cursor.execute(sql, (new_password, user_id))
                self.con.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al actualizar el password del usuario: {e}")
            self.con.rollback()
            return None