from mysql.connector import Error
from app.dao.database import Database
from app.models.cuestionario import Cuestionario, Pregunta, Respuesta


class CuestionarioDAO:

    @staticmethod
    def get_all():
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Cuestionarios")
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Cuestionario(**row) for row in rows]
        except Error as e:
            print(f"Error en CuestionarioDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(idCuestionario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Cuestionarios WHERE idCuestionario = ?",
                (idCuestionario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Cuestionario(**row) if row else None
        except Error as e:
            print(f"Error en CuestionarioDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(cuestionario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Cuestionarios (titulo, tipo, fechaAsignacion)
                     VALUES (?, ?, ?)"""
            cursor.execute(sql, (
                cuestionario.titulo,
                cuestionario.tipo,
                cuestionario.fechaAsignacion
            ))
            conn.commit()
            # JDBC usa getGeneratedKeys en lugar de lastrowid
            keys = cursor._rs
            return keys.getInt(1) if keys and keys.next() else None
        except Error as e:
            print(f"Error en CuestionarioDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(cuestionario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Cuestionarios
                     SET titulo = ?, tipo = ?, fechaAsignacion = ?
                     WHERE idCuestionario = ?"""
            cursor.execute(sql, (
                cuestionario.titulo,
                cuestionario.tipo,
                cuestionario.fechaAsignacion,
                cuestionario.idCuestionario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en CuestionarioDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(idCuestionario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Cuestionarios WHERE idCuestionario = ?",
                (idCuestionario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en CuestionarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class PreguntaDAO:

    @staticmethod
    def get_by_cuestionario(idCuestionario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Preguntas WHERE idCuestionario = ?",
                (idCuestionario,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Pregunta(**row) for row in rows]
        except Error as e:
            print(f"Error en PreguntaDAO.get_by_cuestionario: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(idPregunta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Preguntas WHERE idPregunta = ?",
                (idPregunta,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Pregunta(**row) if row else None
        except Error as e:
            print(f"Error en PreguntaDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pregunta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Preguntas (idCuestionario, enunciado, tipoRespuesta)
                     VALUES (?, ?, ?)"""
            cursor.execute(sql, (
                pregunta.idCuestionario,
                pregunta.enunciado,
                pregunta.tipoRespuesta
            ))
            conn.commit()
            keys = cursor._rs
            return keys.getInt(1) if keys and keys.next() else None
        except Error as e:
            print(f"Error en PreguntaDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(idPregunta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Preguntas WHERE idPregunta = ?",
                (idPregunta,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PreguntaDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class RespuestaDAO:

    @staticmethod
    def get_by_paciente(idPaciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Respuestas WHERE idPaciente = ? ORDER BY fechaHora DESC",
                (idPaciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Respuesta(**row) for row in rows]
        except Error as e:
            print(f"Error en RespuestaDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_pregunta(idPregunta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Respuestas WHERE idPregunta = ? ORDER BY fechaHora DESC",
                (idPregunta,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Respuesta(**row) for row in rows]
        except Error as e:
            print(f"Error en RespuestaDAO.get_by_pregunta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(respuesta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Respuestas (idPregunta, idPaciente, fechaHora, contenido)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
                respuesta.idPregunta,
                respuesta.idPaciente,
                # JDBC no acepta datetime de Python, hay que pasarlo como string
                str(respuesta.fechaHora) if respuesta.fechaHora else None,
                respuesta.contenido
            ))
            conn.commit()
            return True  # devolvemos True en lugar de lastrowid que no existe en JDBC
        except Error as e:
            print(f"Error en RespuestaDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(idRespuesta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Respuestas WHERE idRespuesta = ?",
                (idRespuesta,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en RespuestaDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()