from mysql.connector import Error
from app.dao.database import Database
from app.models.cuestionario import Cuestionario, Pregunta, Respuesta


class CuestionarioDAO:
    """Operaciones sobre la tabla Cuestionarios."""

    @staticmethod
    def get_all():
        """Devuelve todos los cuestionarios."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Cuestionarios")
            return [Cuestionario(**row) for row in cursor.fetchall()]
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

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Cuestionarios WHERE idCuestionario = %s",
                (idCuestionario,)
            )
            row = cursor.fetchone()
            return Cuestionario(**row) if row else None
        except Error as e:
            print(f"Error en CuestionarioDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(cuestionario):
        """Inserta un cuestionario y devuelve el id generado."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Cuestionarios (titulo, tipo, fechaAsignacion)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (
                cuestionario.titulo,
                cuestionario.tipo,
                cuestionario.fechaAsignacion
            ))
            conn.commit()
            return cursor.lastrowid
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
                     SET titulo = %s, tipo = %s, fechaAsignacion = %s
                     WHERE idCuestionario = %s"""
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
                "DELETE FROM Cuestionarios WHERE idCuestionario = %s",
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
    """Operaciones sobre la tabla Preguntas."""

    @staticmethod
    def get_by_cuestionario(idCuestionario):
        """Devuelve todas las preguntas de un cuestionario."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Preguntas WHERE idCuestionario = %s",
                (idCuestionario,)
            )
            return [Pregunta(**row) for row in cursor.fetchall()]
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

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Preguntas WHERE idPregunta = %s",
                (idPregunta,)
            )
            row = cursor.fetchone()
            return Pregunta(**row) if row else None
        except Error as e:
            print(f"Error en PreguntaDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pregunta):
        """Inserta una pregunta y devuelve el id generado."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Preguntas (idCuestionario, enunciado, tipoRespuesta)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (
                pregunta.idCuestionario,
                pregunta.enunciado,
                pregunta.tipoRespuesta
            ))
            conn.commit()
            return cursor.lastrowid
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
                "DELETE FROM Preguntas WHERE idPregunta = %s",
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
    """Operaciones sobre la tabla Respuestas."""

    @staticmethod
    def get_by_paciente(idPaciente):
        """Devuelve todas las respuestas de un paciente."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Respuestas WHERE idPaciente = %s ORDER BY fechaHora DESC",
                (idPaciente,)
            )
            return [Respuesta(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en RespuestaDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_pregunta(idPregunta):
        """Devuelve todas las respuestas de una pregunta."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Respuestas WHERE idPregunta = %s ORDER BY fechaHora DESC",
                (idPregunta,)
            )
            return [Respuesta(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en RespuestaDAO.get_by_pregunta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(respuesta):
        """Inserta una respuesta y devuelve el id generado."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Respuestas (idPregunta, idPaciente, fechaHora, contenido)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (
                respuesta.idPregunta,
                respuesta.idPaciente,
                respuesta.fechaHora,
                respuesta.contenido
            ))
            conn.commit()
            return cursor.lastrowid
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
                "DELETE FROM Respuestas WHERE idRespuesta = %s",
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