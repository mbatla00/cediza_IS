from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Pregunta
from mysql.connector import Error

GET_BY_CUESTIONARIO = "SELECT * FROM Preguntas WHERE idCuestionario = ?"
GET_BY_ID = "SELECT * FROM Preguntas WHERE idPregunta = ?"
CREATE = """INSERT INTO Preguntas (idCuestionario, enunciado, tipoRespuesta)
                     VALUES (?, ?, ?)"""
DELETE = "DELETE FROM Preguntas WHERE idPregunta = ?"


class PreguntaDAO:

    @staticmethod
    def get_by_cuestionario(idCuestionario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_CUESTIONARIO,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ID,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
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