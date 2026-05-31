from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Informe
from mysql.connector import Error

GET_BY_REF = "SELECT * FROM Informe WHERE referencia = ?"
GET_BY_PACIENTE = """SELECT * FROM Informe
                   WHERE Paciente = ? ORDER BY fechaGeneracion DESC"""
CREATE = """INSERT INTO Informe
                     (referencia, Paciente, Trabajador, fechaGeneracion, periodoInicio, periodoFin)
                     VALUES (?, ?, ?, ?, ?, ?)"""
DELETE = "DELETE FROM Informe WHERE referencia = ?"

class InformeDAO:

    @staticmethod
    def get_by_referencia(referencia):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_REF,
                (referencia,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Informe(**row) if row else None
        except Error as e:
            print(f"Error en InformeDAO.get_by_referencia: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_PACIENTE,
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Informe(**row) for row in rows]
        except Error as e:
            print(f"Error en InformeDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(informe):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Convertir fechas para JDBC
            fecha_gen = informe.fechaGeneracion
            periodo_ini = informe.periodoInicio
            periodo_fin = informe.periodoFin
            
            import time
            SQLDate = jpype.JClass("java.sql.Date")
            
            if isinstance(fecha_gen, date):
                timestamp = int(time.mktime(fecha_gen.timetuple()) * 1000)
                fecha_gen = SQLDate(timestamp)
            if isinstance(periodo_ini, date):
                timestamp = int(time.mktime(periodo_ini.timetuple()) * 1000)
                periodo_ini = SQLDate(timestamp)
            if isinstance(periodo_fin, date):
                timestamp = int(time.mktime(periodo_fin.timetuple()) * 1000)
                periodo_fin = SQLDate(timestamp)
            
            cursor.execute(CREATE, (
                informe.referencia,
                informe.paciente,
                informe.trabajador,
                fecha_gen,
                periodo_ini,
                periodo_fin
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en InformeDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(referencia):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (referencia,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en InformeDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()