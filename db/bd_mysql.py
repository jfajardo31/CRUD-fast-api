import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales de la BD
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]

class ConnectDB:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        
        """Establecer y mantener una conexión persistente"""
        if not self.connection or not self.connection.open:  # Verifica si la conexión está activa
            try:
                self.connection = pymysql.connect( 
                    host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER,
                    passwd=MYSQL_PASSWORD, db="nequi"
                )
                print("Conectado a MySQL")
            except Exception as e:
                print(f"Error al conectar: {e}")
        return self.connection

    def close_connection(self):
        """Cierra la conexión solo si está activa"""
        if self.connection and self.connection.open: # Verifica si la conexión está activa
            self.connection.close() #   Cierra la conexión
            print("Conexión cerrada")

# Instancia única de la conexión
db_conn = ConnectDB() 

# Función para obtener la conexión activa
def get_db_connection():
    return db_conn.connect()
