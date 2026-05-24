from mysql.connector import Error
from app.dao.database import Database
from app.models.paciente import Paciente
from app.models.paciente_tipos import PacPub, PacPri


class PacienteDAO:

    @staticmethod
    def get_all():
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []


        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Pacientes")
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Paciente(**row) for row in rows]
        except Error as e:
            print(f"Error en PacienteDAO.get_all: {e}")

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
                "SELECT * FROM Pacientes WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Paciente(**row) if row else None
        except Error as e:
            print(f"Error en PacienteDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Pacientes (nombreUsuario, Tipo) VALUES (?, ?)"
            cursor.execute(sql, (paciente.nombreUsuario, paciente.tipo))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacienteDAO.create: {e}")
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
                "DELETE FROM Pacientes WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacienteDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class PacPubDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Pac_pub WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return PacPub(**row) if row else None
        except Error as e:
            print(f"Error en PacPubDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pac_pub):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Pac_pub (nombreUsuario, Dias_ingresado) VALUES (?, ?)"
            cursor.execute(sql, (pac_pub.nombreUsuario, pac_pub.dias_ingresado))
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Pac_pub SET Dias_ingresado = ? WHERE nombreUsuario = ?",
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


class PacPriDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Pac_pri WHERE nombreUsuario = ?",
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Pac_pri (nombreUsuario, IVA, cuenta, horas)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Pac_pri
                     SET IVA = ?, cuenta = ?, horas = ?
                     WHERE nombreUsuario = ?"""
            cursor.execute(sql, (
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