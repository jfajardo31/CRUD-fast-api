import pymysql
import os
from dotenv import load_dotenv


load_dotenv()

# Credenciales de producción
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]

class ConnectDB:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        #Establecer conexión con la BD
        try:
            self.connection = pymysql.connect(
                host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER,
                passwd=MYSQL_PASSWORD, db="nequi"
            )
            print("Conectado a MySQL")
            return self.connection
            
            
        except Exception as e:
            print(f"Error al conectar: {e}")

 # Cierra la conexión manualmente si es necesario
    def close_connection(self):
        if self.con:
            self.con.close()
    
# Inicializa la conexión a la base de datos
db_conn = ConnectDB()

# Función para obtener la conexión activa
def get_db_connection():
    return db_conn.connect()