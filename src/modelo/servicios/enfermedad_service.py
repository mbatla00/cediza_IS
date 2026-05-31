"""
SERVICIO DE ENFERMEDADES
"""
from src.modelo.conexion.Conexion import Conexion


class EnfermedadService:
    
    @staticmethod
    def listar_todas() -> list:
        db = Conexion()
        conn = db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nombre FROM Enfermedades ORDER BY nombre")
            rows = cursor.fetchall()
            return [{'id': r[0], 'nombre': r[1]} for r in rows]
        finally:
            cursor.close()
    
    @staticmethod
    def crear(nombre: str) -> tuple[bool, str, int | None]:
        db = Conexion()
        conn = db.get_connection()
        if not conn:
            return False, "Error de conexión", None
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Enfermedades (nombre) VALUES (?)", (nombre,))
            conn.commit()
            # JDBC no tiene lastrowid fácil, obtener el ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            return True, "Enfermedad creada", last_id
        except Exception as e:
            return False, str(e), None
        finally:
            cursor.close()
    
    @staticmethod
    def asignar_a_paciente(paciente: str, enfermedad_id: int) -> bool:
        db = Conexion()
        conn = db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO PacienteEnfermedad (paciente, enfermedad_id) VALUES (?, ?)",
                (paciente, enfermedad_id)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def eliminar_de_paciente(paciente: str, enfermedad_id: int) -> bool:
        db = Conexion()
        conn = db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM PacienteEnfermedad WHERE paciente = ? AND enfermedad_id = ?",
                (paciente, enfermedad_id)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            cursor.close()