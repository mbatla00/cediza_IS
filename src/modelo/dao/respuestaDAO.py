from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Respuesta

GET_BY_PACIENTE = "SELECT * FROM Respuestas WHERE idPaciente = ? ORDER BY fechaHora DESC"
GET_BY_PREGUNTA = "SELECT * FROM Respuestas WHERE idPregunta = ? ORDER BY fechaHora DESC"
CREATE = """INSERT INTO Respuestas (idPregunta, idPaciente, fechaHora, contenido)
                     VALUES (?, ?, ?, ?)"""
DELETE = "DELETE FROM Respuestas WHERE idRespuesta = ?"

class RespuestaDAO:

    @staticmethod
    def get_by_paciente(idPaciente):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_PACIENTE,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_PREGUNTA,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            fecha_hora_str = str(respuesta.fechaHora) if respuesta.fechaHora else None
            cursor.execute(CREATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
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