from typing import Optional
from db.bd_mysql import get_db_connection

class BolsilloService:
    
    def __init__(self):
        # Inicializa la conexión al crear una instancia de la clase
        self.con = get_db_connection()
    

    @staticmethod
    async def get_bolsillos(self) -> Optional[list]:
        """_summary_

        Returns:
            list: _description_
        """
        try:
            with self.con.cursor() as cursor:
                sql = "SELECT b.id, b.saldo, u.nombre, u.apellido, u.numtelefono FROM bolsillo b JOIN usuario u ON b.usuario_FK=u.id"
                cursor.execute(sql)
                bolsillos = cursor.fetchall()  # fetchall para obtener todos los registros
                return bolsillos
        except Exception as e:
            print(f"Error al consultar bolsillos: {e}")
            return None

    # Función para crear bolsillos
    async def create_bolsillo(self, bolsillo_data):
        try:
            with self.con.cursor() as cursor:
                sql = "INSERT INTO bolsillo (nombre, saldo, usuario_FK) VALUES (%s, %s,%s)"
                cursor.execute(sql, (bolsillo_data.nombre, bolsillo_data.saldo,bolsillo_data.usuario))
                self.con.commit()                                                                 
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            self.con.rollback()
            return None

    async def get_bolsillo(self):
        try:
            with self.con.cursor() as cursor:
                sql="SELECT b.saldo, u.nombre,u.apellido, u.numtelefono FROM usuario JOIN bolsillo ON b.usuario_FK=u.id WHERE id=%s"
                cursor.execute(sql,(id))
                self.con.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar ekl bolsillo del usuario: {e}")
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


                
