from mysql.connector import Error
from .database import Database
from src.modelo.vo import EvaluacionProfesional, Informe, Factura
from datetime import date
import jpype


class EvaluacionProfesionalDAO:

    @staticmethod
    def get_by_id(idEvaluacion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM EvaluacionProfesional WHERE idEvaluacion = ?",
                (idEvaluacion,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return EvaluacionProfesional(**row) if row else None
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_id: {e}")
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
                """SELECT * FROM EvaluacionProfesional
                   WHERE Paciente = ? ORDER BY fecha DESC""",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [EvaluacionProfesional(**row) for row in rows]
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_paciente: {e}")
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
                """SELECT * FROM EvaluacionProfesional
                   WHERE Trabajador = ? ORDER BY fecha DESC""",
                (nombreUsuario_trabajador,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [EvaluacionProfesional(**row) for row in rows]
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_trabajador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(evaluacion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            # Convertir fecha de Python a java.sql.Date para JDBC
            fecha_a_guardar = evaluacion.fecha
            if isinstance(fecha_a_guardar, date):
                # Convertir datetime.date de Python a java.sql.Date
                SQLDate = jpype.JClass("java.sql.Date")
                # java.sql.Date espera milisegundos desde epoch
                import time
                timestamp = int(time.mktime(fecha_a_guardar.timetuple()) * 1000)
                fecha_a_guardar = SQLDate(timestamp)
            
            sql = """INSERT INTO EvaluacionProfesional
                     (Paciente, Trabajador, fecha, movilidad, estadoEmocional, apetito, observaciones)
                     VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                evaluacion.paciente,
                evaluacion.trabajador,
                fecha_a_guardar,
                evaluacion.movilidad,
                evaluacion.estadoEmocional,
                evaluacion.apetito,
                evaluacion.observaciones
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en EvaluacionProfesionalDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(evaluacion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE EvaluacionProfesional
                     SET movilidad = ?, estadoEmocional = ?,
                         apetito = ?, observaciones = ?
                     WHERE idEvaluacion = ?"""
            cursor.execute(sql, (
                evaluacion.movilidad,
                evaluacion.estadoEmocional,
                evaluacion.apetito,
                evaluacion.observaciones,
                evaluacion.idEvaluacion
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(idEvaluacion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM EvaluacionProfesional WHERE idEvaluacion = ?",
                (idEvaluacion,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class InformeDAO:

    @staticmethod
    def get_by_referencia(referencia):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Informe WHERE referencia = ?",
                (referencia,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Informe(**row) if row else None
        except Error as e:
            print(f"Error en InformeDAO.get_by_referencia: {e}")
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
                """SELECT * FROM Informe
                   WHERE Paciente = ? ORDER BY fechaGeneracion DESC""",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Informe(**row) for row in rows]
        except Error as e:
            print(f"Error en InformeDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(informe):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Convertir fechas para JDBC
            fecha_gen = informe.fechaGeneracion
            periodo_ini = informe.periodoInicio
            periodo_fin = informe.periodoFin
            
            import time
            SQLDate = jpype.JClass("java.sql.Date")
            
            if isinstance(fecha_gen, date):
                timestamp = int(time.mktime(fecha_gen.timetuple()) * 1000)
                fecha_gen = SQLDate(timestamp)
            if isinstance(periodo_ini, date):
                timestamp = int(time.mktime(periodo_ini.timetuple()) * 1000)
                periodo_ini = SQLDate(timestamp)
            if isinstance(periodo_fin, date):
                timestamp = int(time.mktime(periodo_fin.timetuple()) * 1000)
                periodo_fin = SQLDate(timestamp)
            
            sql = """INSERT INTO Informe
                     (referencia, Paciente, Trabajador, fechaGeneracion, periodoInicio, periodoFin)
                     VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                informe.referencia,
                informe.paciente,
                informe.trabajador,
                fecha_gen,
                periodo_ini,
                periodo_fin
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en InformeDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(referencia):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Informe WHERE referencia = ?",
                (referencia,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en InformeDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class FacturaDAO:

    @staticmethod
    def get_by_codigo(codigoFactura):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Factura WHERE codigoFactura = ?",
                (codigoFactura,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Factura(**row) if row else None
        except Error as e:
            print(f"Error en FacturaDAO.get_by_codigo: {e}")
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
                """SELECT * FROM Factura
                   WHERE Paciente = ? ORDER BY fechaEmision DESC""",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Factura(**row) for row in rows]
        except Error as e:
            print(f"Error en FacturaDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_administrador(nombreUsuario_admin):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                """SELECT * FROM Factura
                   WHERE Administrador = ? ORDER BY fechaEmision DESC""",
                (nombreUsuario_admin,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Factura(**row) for row in rows]
        except Error as e:
            print(f"Error en FacturaDAO.get_by_administrador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(factura):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Convertir fecha para JDBC
            fecha_emision = factura.fechaEmision
            if isinstance(fecha_emision, date):
                import time
                SQLDate = jpype.JClass("java.sql.Date")
                timestamp = int(time.mktime(fecha_emision.timetuple()) * 1000)
                fecha_emision = SQLDate(timestamp)
            
            sql = """INSERT INTO Factura
                     (codigoFactura, Paciente, Administrador, fechaEmision, importeTotal, estadoPago)
                     VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                factura.codigoFactura,
                factura.paciente,
                factura.administrador,
                fecha_emision,
                factura.importeTotal,
                factura.estadoPago
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_estado(codigoFactura, estadoPago):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Factura SET estadoPago = ? WHERE codigoFactura = ?",
                (estadoPago, codigoFactura)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.update_estado: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_importe(codigoFactura, importeTotal):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Factura SET importeTotal = ? WHERE codigoFactura = ?",
                (importeTotal, codigoFactura)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.update_importe: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(codigoFactura):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Factura WHERE codigoFactura = ?",
                (codigoFactura,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()