from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import EvaluacionProfesional

GET_BY_ID = "SELECT * FROM EvaluacionProfesional WHERE idEvaluacion = ?"
GET_BY_PACIENTE = """SELECT * FROM EvaluacionProfesional
                   WHERE Paciente = ? ORDER BY fecha DESC"""
GET_BY_TRABAJADOR = """SELECT * FROM EvaluacionProfesional
                   WHERE Trabajador = ? ORDER BY fecha DESC"""
CREATE = """INSERT INTO EvaluacionProfesional
                     (Paciente, Trabajador, fecha, movilidad, estadoEmocional, apetito, observaciones)
                     VALUES (?, ?, ?, ?, ?, ?, ?)"""
UPDATE = """UPDATE EvaluacionProfesional
                     SET movilidad = ?, estadoEmocional = ?,
                         apetito = ?, observaciones = ?
                     WHERE idEvaluacion = ?"""
DELETE = "DELETE FROM EvaluacionProfesional WHERE idEvaluacion = ?"

class EvaluacionProfesionalDAO:

    @staticmethod
    def get_by_id(idEvaluacion):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ID,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_PACIENTE,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_TRABAJADOR,
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
        db = Conexion()
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
            
            cursor.execute(CREATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(UPDATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
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