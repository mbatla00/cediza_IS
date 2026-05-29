from mysql.connector import Error
from .database import Database
from src.modelo.vo import Trabajador, Auxiliar, Coordinador, Especialista



class TrabajadorDAO:

    @staticmethod
    def get_all():
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Trabajadores")
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Trabajador(**row) for row in rows]
        except Error as e:
            print(f"Error en TrabajadorDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Trabajadores WHERE nombreUsuario = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Trabajadores (nombreUsuario, Tipo) VALUES (?, ?)"
            cursor.execute(sql, (trabajador.nombreUsuario, trabajador.tipo))
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Trabajadores WHERE nombreUsuario = ?",
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


class AuxiliarDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Auxiliares WHERE nombreUsuario = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Auxiliares")
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Auxiliar(**row) for row in rows]
        except Error as e:
            print(f"Error en AuxiliarDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(auxiliar):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Auxiliares (nombreUsuario, Horario) VALUES (?, ?)"
            cursor.execute(sql, (auxiliar.nombreUsuario, auxiliar.horario))
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Auxiliares SET Horario = ? WHERE nombreUsuario = ?",
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


class CoordinadorDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM coordinadores WHERE nombreUsuario = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO coordinadores (nombreUsuario, infoInteres) VALUES (?, ?)"
            cursor.execute(sql, (coordinador.nombreUsuario, coordinador.infoInteres))
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE coordinadores SET infoInteres = ? WHERE nombreUsuario = ?",
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


class EspecialistaDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Especialistas WHERE nombreUsuario = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Especialistas")
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Especialista(**row) for row in rows]
        except Error as e:
            print(f"Error en EspecialistaDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(especialista):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Especialistas (nombreUsuario, Especialidad, Horario)
                     VALUES (?, ?, ?)"""
            cursor.execute(sql, (
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Especialistas
                     SET Especialidad = ?, Horario = ?
                     WHERE nombreUsuario = ?"""
            cursor.execute(sql, (
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