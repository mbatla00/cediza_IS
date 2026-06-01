from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo.enfermedadVO import Enfermedad

GET_ALL = "SELECT * FROM enfermedades"
GET_BY_ID = "SELECT * FROM enfermedades WHERE id = ?"
GET_BY_PACIENTE = """SELECT e.* FROM enfermedades e
                     JOIN pacienteenfermedad pe ON e.id = pe.enfermedad_id
                     WHERE pe.paciente = ?"""
CREATE = "INSERT INTO enfermedades (nombre) VALUES (?)"
DELETE = "DELETE FROM enfermedades WHERE id = ?"



class EnfermedadDAO:

    @staticmethod
    def get_all():
        conn = Database().get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(GET_ALL)
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            return [Enfermedad(**dict(zip(columns, row))) for row in rows]
        except Exception as e:
            print(f"Error en EnfermedadDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(id):
        conn = Database().get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_ID, (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0].split('.')[-1] for col in cursor.description]
            return Enfermedad(**dict(zip(columns, row)))
        except Exception as e:
            print(f"Error en EnfermedadDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario):
        """Devuelve todas las enfermedades de un paciente."""
        conn = Database().get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_PACIENTE, (nombreUsuario,))
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            return [Enfermedad(**dict(zip(columns, row))) for row in rows]
        except Exception as e:
            print(f"Error en EnfermedadDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(enfermedad):
        conn = Database().get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (enfermedad.nombre,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en EnfermedadDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(id):
        conn = Database().get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(DELETE, (id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en EnfermedadDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()