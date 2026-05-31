from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Paciente
from mysql.connector import Error


class PacienteDAO:

    @staticmethod
    def get_all():
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.*, u.Nombre, u.activo 
                FROM Pacientes p
                JOIN Usuarios u ON p.nombreUsuario = u.nombreUsuario
                WHERE u.activo = 1
            """) 
            raw_rows = cursor.fetchall()
            
            pacientes = []
            for raw_row in raw_rows:
                row_raw = Conexion.row_to_dict(cursor, raw_row)
                if not row_raw:
                    continue
                
                row = {k.lower(): v for k, v in row_raw.items()}
                
                paciente_obj = Paciente(
                    nombreUsuario=row.get('nombreusuario'),
                    Nombre=row.get('nombre'),  # Esto trae el nombre de Usuarios
                    DNI=row.get('dni'),
                    fechaNacimiento=row.get('fechanacimiento'),
                    email=row.get('email'),
                    activo=row.get('activo'),
                    Tipo=row.get('tipo'),           
                    diagnostico=row.get('diagnostico') 
                )
                pacientes.append(paciente_obj)
                
            return pacientes
        except Exception as e:
            print(f"Error crítico en PacienteDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.*, u.Nombre, u.activo 
                FROM Pacientes p
                JOIN Usuarios u ON p.nombreUsuario = u.nombreUsuario
                WHERE p.nombreUsuario = ?
            """, (nombreUsuario,))
            raw_row = cursor.fetchone()
            
            if raw_row:
                row_raw = Database.row_to_dict(cursor, raw_row)
                if not row_raw:
                    return None
                
                row = {k.lower(): v for k, v in row_raw.items()}
                
                return Paciente(
                    nombreUsuario=row.get('nombreusuario'),
                    Nombre=row.get('nombre'),  # Esto trae el nombre de Usuarios
                    DNI=row.get('dni'),
                    fechaNacimiento=row.get('fechanacimiento'),
                    email=row.get('email'),
                    activo=row.get('activo'),
                    Tipo=row.get('tipo'),           
                    diagnostico=row.get('diagnostico') 
                )
            return None
        except Exception as e:
            print(f"Error crítico en PacienteDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(paciente):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Pacientes (nombreUsuario, Tipo) VALUES (?, ?)"
            cursor.execute(sql, (paciente.nombreUsuario, paciente.tipo))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacienteDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Pacientes WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacienteDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()




