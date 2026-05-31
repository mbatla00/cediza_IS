from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Auxiliar
from mysql.connector import Error

GET_BY_USER = "SELECT * FROM Auxiliares WHERE nombreUsuario = ?"
GET_ALL = "SELECT * FROM Auxiliares"
CREATE = "INSERT INTO Auxiliares (nombreUsuario, Horario) VALUES (?, ?)"
UPDATE_HORARIO = "UPDATE Auxiliares SET Horario = ? WHERE nombreUsuario = ?"

class AuxiliarDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_USER,
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Auxiliar(**row) if row else None
        except Error as e:
            print(f"Error en AuxiliarDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(GET_ALL)
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Auxiliar(**row) for row in rows]
        except Error as e:
            print(f"Error en AuxiliarDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(auxiliar):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (auxiliar.nombreUsuario, auxiliar.horario))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en AuxiliarDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_horario(nombreUsuario, horario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                UPDATE_HORARIO,
                (horario, nombreUsuario)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en AuxiliarDAO.update_horario: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

