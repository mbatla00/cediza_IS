from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Especialista

GET_BY_USER = "SELECT * FROM Especialistas WHERE nombreUsuario = ?"
GET_ALL = "SELECT * FROM Especialistas"
CREATE = """INSERT INTO Especialistas (nombreUsuario, Especialidad, Horario)
                     VALUES (?, ?, ?)"""
UPDATE = """UPDATE Especialistas
                     SET Especialidad = ?, Horario = ?
                     WHERE nombreUsuario = ?"""


class EspecialistaDAO:

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
            return Especialista(**row) if row else None
        except Error as e:
            print(f"Error en EspecialistaDAO.get_by_nombreUsuario: {e}")
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
            return [Especialista(**row) for row in rows]
        except Error as e:
            print(f"Error en EspecialistaDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(especialista):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
                especialista.nombreUsuario,
                especialista.especialidad,
                especialista.horario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en EspecialistaDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update(especialista):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(UPDATE, (
                especialista.especialidad,
                especialista.horario,
                especialista.nombreUsuario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en EspecialistaDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()