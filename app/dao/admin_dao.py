from app.dao.database import Database
from mysql.connector import Error


class AdministradorDAO:
    """Operaciones sobre la tabla Administrador."""

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                """SELECT u.*, a.nombreUsuario as adminUser
                   FROM Usuarios u
                   JOIN Administrador a ON u.nombreUsuario = a.nombreUsuario
                   WHERE u.nombreUsuario = ?""",
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            from app.models.administrador import Administrador
            return Administrador(**{k: v for k, v in row.items()
                                    if k != 'adminUser'}) if row else None
        except Error as e:
            print(f"Error en AdministradorDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(admin):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Administrador (nombreUsuario) VALUES (?)",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Administrador WHERE nombreUsuario = ?",
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