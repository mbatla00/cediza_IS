from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Comentario
from mysql.connector import Error

"""
Tabla de comentarios:
Comentarios libres de trabajadores a pacientes
"""

GET_BY_PACIENTE = "SELECT idComentario AS id, Auxiliar, Paciente, dia, nota FROM comentarios WHERE Paciente = ? ORDER BY dia DESC"
GET_BY_TRABAJADOR = "SELECT idComentario AS id, Auxiliar, Paciente, dia, nota FROM comentarios WHERE Auxiliar = ? ORDER BY dia DESC"
CREATE = """INSERT INTO comentarios (Auxiliar, Paciente, dia, nota) VALUES (?, ?, ?, ?)"""
DELETE = "DELETE FROM comentarios WHERE idComentario = ?"

class ComentarioDAO:

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_PACIENTE, (nombreUsuario_paciente,))
            rows = cursor.fetchall()
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'nota': row[4]
                }
                comentarios.append(Comentario(**row_dict))
            return comentarios
        except Exception as e:
            print(f"Error en ComentarioDAO.get_by_paciente: {e}")
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
            cursor.execute(GET_BY_TRABAJADOR, (nombreUsuario_trabajador,))
            rows = cursor.fetchall()
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'nota': row[4]
                }
                comentarios.append(Comentario(**row_dict))
            return comentarios
        except Exception as e:
            print(f"Error en ComentarioDAO.get_by_trabajador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(comentario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            dia_str = str(comentario.dia) if comentario.dia else None
            cursor.execute(CREATE, (
                comentario.auxiliar,
                comentario.paciente,
                dia_str,
                comentario.nota
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en ComentarioDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(idComentrio):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(DELETE, (idComentrio,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()