from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import PacPri

GET_BY_USER = "SELECT * FROM Pac_pri WHERE nombreUsuario = ?"
CREATE = """INSERT INTO Pac_pri (nombreUsuario, IVA, cuenta, horas)
                     VALUES (?, ?, ?, ?)"""
UPDATE = """UPDATE Pac_pri
                     SET IVA = ?, cuenta = ?, horas = ?
                     WHERE nombreUsuario = ?"""

class PacPriDAO:

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
            return PacPri(**row) if row else None
        except Error as e:
            print(f"Error en PacPriDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pac_pri):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
                pac_pri.nombreUsuario,
                pac_pri.iva,
                pac_pri.cuenta,
                pac_pri.horas
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPriDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update(pac_pri):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(UPDATE, (
                pac_pri.iva,
                pac_pri.cuenta,
                pac_pri.horas,
                pac_pri.nombreUsuario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPriDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()