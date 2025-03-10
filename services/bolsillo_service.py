from typing import Optional, List
from fastapi.responses import JSONResponse
import pymysql
from db.bd_mysql import get_db_connection

class BolsilloService:
    
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.con = get_db_connection()
        if self.con is None:
            raise Exception("No se pudo establecer conexión con la base de datos")
    
    async def get_bolsillos(self):
        """Consulta todos los bolsillos y devuelve JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:  # Retornar como diccionario
                sql = """SELECT b.id, b.saldo, u.nombre, u.apellido, u.numtelefono 
                         FROM bolsillo b 
                         JOIN usuario u ON b.usuario_FK = u.id"""
                cursor.execute(sql)
                bolsillos = cursor.fetchall()

                return JSONResponse(content={"success": True, "data": bolsillos}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"success": False, "message": f"Error al consultar bolsillos: {str(e)}"}, status_code=500)
    
    async def get_bolsillo(self, user_id: int):
        """Consulta el bolsillo de un usuario específico."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """SELECT b.saldo, u.nombre, u.apellido, u.numtelefono 
                         FROM bolsillo b 
                         JOIN usuario u ON b.usuario_FK = u.id 
                         WHERE u.id = %s"""
                cursor.execute(sql, (user_id,))
                bolsillo = cursor.fetchone()

                if bolsillo:
                    return JSONResponse(content={"success": True, "data": bolsillo}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "Bolsillo no encontrado."}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"success": False, "message": f"Error al consultar el bolsillo: {str(e)}"}, status_code=500)

    async def create_bolsillo(self, bolsillo_data):
        """Crea un bolsillo y devuelve JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = "INSERT INTO bolsillo (nombre, saldo, usuario_FK) VALUES (%s, %s, %s)"
                cursor.execute(sql, (bolsillo_data.nombre, bolsillo_data.saldo, bolsillo_data.usuario))
                self.con.commit()

                if cursor.lastrowid:
                    return JSONResponse(content={"success": True, "message": "Bolsillo creado correctamente.", "id": cursor.lastrowid}, status_code=201)
                else:
                    return JSONResponse(content={"success": False, "message": "No se pudo crear el bolsillo."}, status_code=400)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al crear bolsillo: {str(e)}"}, status_code=500)
    
    def close_connection(self):
        """Cierra la conexión con la base de datos."""
        if self.con:
            self.con.close()
