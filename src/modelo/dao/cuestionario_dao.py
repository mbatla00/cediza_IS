from .database import Database
from src.modelo.vo import Cuestionario, Pregunta, Respuesta


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
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            cuestionarios = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                cuestionario = Cuestionario(
                    idCuestionario=row_dict.get('idCuestionario'),
                    titulo=row_dict.get('titulo'),
                    tipo=row_dict.get('tipo'),
                    fechaAsignacion=row_dict.get('fechaAsignacion')
                )
                cuestionarios.append(cuestionario)
            return cuestionarios
        except Exception as e:
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
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0].split('.')[-1] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            return Cuestionario(
                idCuestionario=row_dict.get('idCuestionario'),
                titulo=row_dict.get('titulo'),
                tipo=row_dict.get('tipo'),
                fechaAsignacion=row_dict.get('fechaAsignacion')
            )
        except Exception as e:
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
            return True  # JDBC no tiene lastrowid
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            preguntas = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                pregunta = Pregunta(
                    idPregunta=row_dict.get('idPregunta'),
                    idCuestionario=row_dict.get('idCuestionario'),
                    enunciado=row_dict.get('enunciado'),
                    tipoRespuesta=row_dict.get('tipoRespuesta')
                )
                preguntas.append(pregunta)
            return preguntas
        except Exception as e:
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
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0].split('.')[-1] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            return Pregunta(
                idPregunta=row_dict.get('idPregunta'),
                idCuestionario=row_dict.get('idCuestionario'),
                enunciado=row_dict.get('enunciado'),
                tipoRespuesta=row_dict.get('tipoRespuesta')
            )
        except Exception as e:
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
            return True  # JDBC no tiene lastrowid
        except Exception as e:
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
        except Exception as e:
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
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            respuestas = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                respuesta = Respuesta(
                    idRespuesta=row_dict.get('idRespuesta'),
                    idPregunta=row_dict.get('idPregunta'),
                    idPaciente=row_dict.get('idPaciente'),
                    fechaHora=row_dict.get('fechaHora'),
                    contenido=row_dict.get('contenido')
                )
                respuestas.append(respuesta)
            return respuestas
        except Exception as e:
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
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            respuestas = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                respuesta = Respuesta(
                    idRespuesta=row_dict.get('idRespuesta'),
                    idPregunta=row_dict.get('idPregunta'),
                    idPaciente=row_dict.get('idPaciente'),
                    fechaHora=row_dict.get('fechaHora'),
                    contenido=row_dict.get('contenido')
                )
                respuestas.append(respuesta)
            return respuestas
        except Exception as e:
            print(f"Error en RespuestaDAO.get_by_pregunta: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(respuesta):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Respuestas (idPregunta, idPaciente, fechaHora, contenido)
                     VALUES (?, ?, ?, ?)"""
            fecha_hora_str = str(respuesta.fechaHora) if respuesta.fechaHora else None
            cursor.execute(sql, (
                respuesta.idPregunta,
                respuesta.idPaciente,
                fecha_hora_str,
                respuesta.contenido
            ))
            conn.commit()
            return True  # ← CORREGIDO: devuelve True si se guardó bien
        except Exception as e:
            print(f"Error en RespuestaDAO.create: {e}")
            conn.rollback()
            return False
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
        except Exception as e:
            print(f"Error en RespuestaDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()