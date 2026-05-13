#-------------------------------------------
# conexión a MySQL con patron Singleton
#-------------------------------------------
#                   OJO: hay que usas JayDeBe pero primero se prueba si funciona esto

import mysql.connector
from mysql.connector import Error
from app.config import Config #Falta!!!!

class Database:
    _instane = None
    _connection = None

    def __new__(cls):
        if cls._instane is None:
            cls._instane = super().__new__(cls)
        return cls._instane

    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    pool_name="cediza_pool",
                    pool_size=5
                )
                print("✅ conexion a MySQL establecida")
            except Error as e:
                print("❌ Error de conexión: {e}")
                return None
        return self._connection

    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("conexion cerrada.")
