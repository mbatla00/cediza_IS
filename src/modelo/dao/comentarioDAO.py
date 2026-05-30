from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Comentario

GET_BY_PACIENTE = "SELECT id, Auxiliar, Paciente, dia, hora, nota FROM comentarios WHERE Paciente = ? ORDER BY dia DESC, hora DESC"
GET_BY_TRABAJADOR = "SELECT id, Auxiliar, Paciente, dia, hora, nota FROM comentarios WHERE Auxiliar = ? ORDER BY dia DESC, hora DESC"
CREATE = """INSERT INTO comentarios (Auxiliar, Paciente, dia, hora, nota)
                     VALUES (?, ?, ?, ?, ?)"""
DELETE = "DELETE FROM comentarios WHERE Auxiliar = ? AND Paciente = ? AND dia = ?"

class ComentarioDAO:

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
            rows = cursor.fetchall()
            
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'hora': row[4],
                    'nota': row[5]
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
            cursor.execute(
                GET_BY_TRABAJADOR,
                (nombreUsuario_trabajador,)
            )
            rows = cursor.fetchall()
            
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'hora': row[4],
                    'nota': row[5]
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
            hora_str = str(comentario.hora) if comentario.hora else None
            
            cursor.execute(CREATE, (
                comentario.auxiliar,
                comentario.paciente,
                dia_str,
                hora_str,
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
    def delete(auxiliar, paciente, dia):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (auxiliar, paciente, dia)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
