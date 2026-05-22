from mysql.connector import Error
from app.dao.database import Database
from app.models.eval_inf_fac import EvaluacionProfesional, Informe, Factura


class EvaluacionProfesionalDAO:
    """Operaciones sobre la tabla EvaluacionProfesional."""

    @staticmethod
    def get_by_id(idEvaluacion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM EvaluacionProfesional WHERE idEvaluacion = %s",
                (idEvaluacion,)
            )
            row = cursor.fetchone()
            return EvaluacionProfesional(**row) if row else None
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        """Devuelve todas las evaluaciones de un paciente ordenadas por fecha."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM EvaluacionProfesional
                   WHERE Paciente = %s ORDER BY fecha DESC""",
                (nombreUsuario_paciente,)
            )
            return [EvaluacionProfesional(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_trabajador(nombreUsuario_trabajador):
        """Devuelve todas las evaluaciones hechas por un trabajador."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM EvaluacionProfesional
                   WHERE Trabajador = %s ORDER BY fecha DESC""",
                (nombreUsuario_trabajador,)
            )
            return [EvaluacionProfesional(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en EvaluacionProfesionalDAO.get_by_trabajador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(evaluacion):
        """Inserta una evaluación y devuelve el id generado."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO EvaluacionProfesional
                     (Paciente, Trabajador, fecha, movilidad, estadoEmocional, apetito, observaciones)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                evaluacion.paciente,
                evaluacion.trabajador,
                evaluacion.fecha,
                evaluacion.movilidad,
                evaluacion.estadoEmocional,
                evaluacion.apetito,
                evaluacion.observaciones
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
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
                     SET movilidad = %s, estadoEmocional = %s,
                         apetito = %s, observaciones = %s
                     WHERE idEvaluacion = %s"""
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
                "DELETE FROM EvaluacionProfesional WHERE idEvaluacion = %s",
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
    """Operaciones sobre la tabla Informe."""

    @staticmethod
    def get_by_referencia(referencia):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Informe WHERE referencia = %s",
                (referencia,)
            )
            row = cursor.fetchone()
            return Informe(**row) if row else None
        except Error as e:
            print(f"Error en InformeDAO.get_by_referencia: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        """Devuelve todos los informes de un paciente."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM Informe
                   WHERE Paciente = %s ORDER BY fechaGeneracion DESC""",
                (nombreUsuario_paciente,)
            )
            return [Informe(**row) for row in cursor.fetchall()]
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
            sql = """INSERT INTO Informe
                     (referencia, Paciente, Trabajador, fechaGeneracion, periodoInicio, periodoFin)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                informe.referencia,
                informe.paciente,
                informe.trabajador,
                informe.fechaGeneracion,
                informe.periodoInicio,
                informe.periodoFin
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
                "DELETE FROM Informe WHERE referencia = %s",
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
    """Operaciones sobre la tabla Factura."""

    @staticmethod
    def get_by_codigo(codigoFactura):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Factura WHERE codigoFactura = %s",
                (codigoFactura,)
            )
            row = cursor.fetchone()
            return Factura(**row) if row else None
        except Error as e:
            print(f"Error en FacturaDAO.get_by_codigo: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        """Devuelve todas las facturas de un paciente."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM Factura
                   WHERE Paciente = %s ORDER BY fechaEmision DESC""",
                (nombreUsuario_paciente,)
            )
            return [Factura(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en FacturaDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_administrador(nombreUsuario_admin):
        """Devuelve todas las facturas gestionadas por un administrador."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM Factura
                   WHERE Administrador = %s ORDER BY fechaEmision DESC""",
                (nombreUsuario_admin,)
            )
            return [Factura(**row) for row in cursor.fetchall()]
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
            sql = """INSERT INTO Factura
                     (codigoFactura, Paciente, Administrador, fechaEmision, importeTotal, estadoPago)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                factura.codigoFactura,
                factura.paciente,
                factura.administrador,
                factura.fechaEmision,
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
        """Actualiza el estado de pago de una factura."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Factura SET estadoPago = %s WHERE codigoFactura = %s",
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
        """Actualiza el importe total de una factura."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Factura SET importeTotal = %s WHERE codigoFactura = %s",
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
                "DELETE FROM Factura WHERE codigoFactura = %s",
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