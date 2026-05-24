from mysql.connector import Error
from app.dao.database import Database
from app.models.familiar import Familiar
from app.models.comentarios import Comentario
from app.models.sesion import Sesion


class FamiliarDAO:

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Familiares WHERE Paciente = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Familiares (Nombre, Paciente, Relacion, Telefono)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Familiares WHERE Nombre = ? AND Paciente = ?",
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


class ComentarioDAO:

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Paciente = ? ORDER BY dia DESC",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Comentario(**row) for row in rows]
        except Error as e:
            print(f"Error en ComentarioDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_trabajador(nombreUsuario_trabajador):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Auxiliar = ? ORDER BY dia DESC",
                (nombreUsuario_trabajador,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Comentario(**row) for row in rows]
        except Error as e:
            print(f"Error en ComentarioDAO.get_by_trabajador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(comentario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO comentarios (Auxiliar, Paciente, dia, nota)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
                comentario.auxiliar,
                comentario.paciente,
                comentario.dia,
                comentario.nota
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(auxiliar, paciente, dia):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM comentarios WHERE Auxiliar = ? AND Paciente = ? AND dia = ?",
                (auxiliar, paciente, dia)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class SesionDAO:

    @staticmethod
    def get_by_id(idSesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE idSesion = ?",
                (idSesion,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Sesion(**row) if row else None
        except Error as e:
            print(f"Error en SesionDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE Paciente = ? ORDER BY Fecha ASC",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Sesion(**row) for row in rows]
        except Error as e:
            print(f"Error en SesionDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_especialista(nombreUsuario_especialista):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE Especialista = ? ORDER BY Fecha ASC",
                (nombreUsuario_especialista,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Sesion(**row) for row in rows]
        except Error as e:
            print(f"Error en SesionDAO.get_by_especialista: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(sesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Sesion (Paciente, Especialista, comentarios, Fecha)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                sesion.fecha
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error en SesionDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(sesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Sesion
                     SET Paciente = ?, Especialista = ?, comentarios = ?, Fecha = ?
                     WHERE idSesion = ?"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                sesion.fecha,
                sesion.idSesion
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en SesionDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(idSesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Sesion WHERE idSesion = ?",
                (idSesion,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en SesionDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
                    