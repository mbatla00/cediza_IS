from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Coordinador
from mysql.connector import Error

GET_BY_USER = "SELECT * FROM coordinadores WHERE nombreUsuario = ?"
CREATE = "INSERT INTO coordinadores (nombreUsuario, infoInteres) VALUES (?, ?)"
UPDATE_INFO = "UPDATE coordinadores SET infoInteres = ? WHERE nombreUsuario = ?"


class CoordinadorDAO:

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
            return Coordinador(**row) if row else None
        except Error as e:
            print(f"Error en CoordinadorDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(coordinador):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (coordinador.nombreUsuario, coordinador.infoInteres))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en CoordinadorDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_infoInteres(nombreUsuario, infoInteres):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                UPDATE_INFO,
                (infoInteres, nombreUsuario)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en CoordinadorDAO.update_infoInteres: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

