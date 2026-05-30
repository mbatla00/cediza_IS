from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import PacPub

GET_BY_USER = "SELECT * FROM Pac_pub WHERE nombreUsuario = ?"
CREATE = "INSERT INTO Pac_pub (nombreUsuario, Dias_ingresado) VALUES (?, ?)"
UPDATE_DIAS = "UPDATE Pac_pub SET Dias_ingresado = ? WHERE nombreUsuario = ?"

class PacPubDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_USER, (nombreUsuario,))
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return PacPub(**row) if row else None
        except Error as e:
            print(f"Error en PacPubDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pac_pub):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (pac_pub.nombreUsuario, pac_pub.dias_ingresado))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPubDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_dias(nombreUsuario, dias_ingresado):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                UPDATE_DIAS,
                (dias_ingresado, nombreUsuario)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPubDAO.update_dias: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
