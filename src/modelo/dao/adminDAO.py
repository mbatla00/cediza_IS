from src.modelo.conexion.Conexion import Conexion
from mysql.connector import Error
from src.modelo.vo import Admin

# QUERIES
GET_BY_USERNAME = """SELECT u.*, a.nombreUsuario as adminUser
                   FROM Usuarios u
                   JOIN Administrador a ON u.nombreUsuario = a.nombreUsuario
                   WHERE u.nombreUsuario = ?"""
CREATE = "INSERT INTO Administrador (nombreUsuario) VALUES (?)"
DELETE = "DELETE FROM Administrador WHERE nombreUsuario = ?"


class AdministradorDAO:
    """Operaciones sobre la tabla Administrador."""

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_USERNAME,
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Admin(**{k: v for k, v in row.items()
                                    if k != 'adminUser'}) if row else None
        except Error as e:
            print(f"Error en AdministradorDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(admin):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                CREATE,
                (admin.nombreUsuario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en AdministradorDAO.create: {e}")
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
            print(f"Error en AdministradorDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()