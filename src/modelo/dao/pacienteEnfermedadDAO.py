from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo.pacienteEnfermedadVO import PacienteEnfermedad

GET_BY_PACIENTE = "SELECT * FROM pacienteenfermedad WHERE paciente = ?"
GET_BY_ENFERMEDAD = "SELECT * FROM pacienteenfermedad WHERE enfermedad_id = ?"
CREATE = "INSERT INTO pacienteenfermedad (paciente, enfermedad_id) VALUES (?, ?)"
DELETE = "DELETE FROM pacienteenfermedad WHERE paciente = ? AND enfermedad_id = ?"



class PacienteEnfermedadDAO:

    @staticmethod
    def get_by_paciente(nombreUsuario):
        conn = Database().get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_PACIENTE, (nombreUsuario,))
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            return [PacienteEnfermedad(**dict(zip(columns, row))) for row in rows]
        except Exception as e:
            print(f"Error en PacienteEnfermedadDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_enfermedad(enfermedad_id):
        conn = Database().get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_ENFERMEDAD, (enfermedad_id,))
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            return [PacienteEnfermedad(**dict(zip(columns, row))) for row in rows]
        except Exception as e:
            print(f"Error en PacienteEnfermedadDAO.get_by_enfermedad: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(paciente_enfermedad):
        """Asocia una enfermedad a un paciente."""
        conn = Database().get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
                paciente_enfermedad.paciente,
                paciente_enfermedad.enfermedad_id
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en PacienteEnfermedadDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(nombreUsuario, enfermedad_id):
        """Elimina la asociación entre un paciente y una enfermedad."""
        conn = Database().get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(DELETE, (nombreUsuario, enfermedad_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en PacienteEnfermedadDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()