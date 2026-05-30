from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Trabajador

GET_ALL = "SELECT * FROM Trabajadores"
GET_BY_USER = "SELECT * FROM Trabajadores WHERE nombreUsuario = ?"
CREATE = "INSERT INTO Trabajadores (nombreUsuario, Tipo) VALUES (?, ?)"
DELETE = "DELETE FROM Trabajadores WHERE nombreUsuario = ?"



class TrabajadorDAO:

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
            return [Trabajador(**row) for row in rows]
        except Error as e:
            print(f"Error en TrabajadorDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

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
            return Trabajador(**row) if row else None
        except Error as e:
            print(f"Error en TrabajadorDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(trabajador):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (trabajador.nombreUsuario, trabajador.tipo))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en TrabajadorDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (nombreUsuario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en TrabajadorDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


