#-------------------------------------------
# conexión a MySQL con patron Singleton
#-------------------------------------------


#-----------------------
#conexion con jdbc
#-----------------------
import jaydebeapi
from src.config import Config

class Conexion:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self):
        if self._connection is None:
            try:
                jdbc_driver = "com.mysql.cj.jdbc.Driver"
                jar_file = "lib/mysql-connector-j-9.7.0.jar"  
                self._connection = jaydebeapi.connect(
                    jdbc_driver,
                    f"jdbc:mysql://localhost/cediza",
                    [Config.MYSQL_USER, Config.MYSQL_PASSWORD],
                    jar_file
                )
                # Obliga a JDBC a esperar el .commit() manual de los DAOs para que no se repitan
                self._connection.jconn.setAutoCommit(False)
                print("✅ Conexión JDBC a MySQL establecida")
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
                return None
        return self._connection


    @staticmethod
    def row_to_dict(cursor, row):
        if row is None:
            return None
        
        # 🛡️ CORRECCIÓN JDBC: Limpiamos prefijos de tablas/alias (ej: 'p.nombreUsuario' -> 'nombreUsuario')
        columns = [col[0].split('.')[-1] for col in cursor.description]
        
        res = dict(zip(columns, row))
        
        extended_res = {}
        for k, v in res.items():
            extended_res[k] = v          
            extended_res[k.lower()] = v  
            
            # Mantenemos la compatibilidad de mayúsculas/minúsculas para el Tipo
            if k.lower() == 'tipo':
                extended_res['Tipo'] = v
                extended_res['TipoPaciente'] = v
                
        return extended_res

    @staticmethod
    def rows_to_dict(cursor, rows):
        if rows is None:
            return []
        return [Database.row_to_dict(cursor, row) for row in rows]


    @staticmethod
    def rows_to_dict(cursor, rows):
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]




    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("🔌 Conexión cerrada")