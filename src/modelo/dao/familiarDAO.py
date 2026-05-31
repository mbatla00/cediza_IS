from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Familiar
from mysql.connector import Error

GET_BY_PACIENTE = "SELECT * FROM Familiares WHERE Paciente = ?"
CREATE = """INSERT INTO Familiares (Nombre, Paciente, Relacion, Telefono)
                     VALUES (?, ?, ?, ?)"""
DELETE = "DELETE FROM Familiares WHERE Nombre = ? AND Paciente = ?"

class FamiliarDAO:

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
            return [Familiar(**row) for row in rows]
        except Error as e:
            print(f"Error en FamiliarDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(familiar):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
                familiar.nombre,
                familiar.paciente,
                familiar.relacion,
                familiar.telefono
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FamiliarDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(nombre, nombreUsuario_paciente):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (nombre, nombreUsuario_paciente)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FamiliarDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()