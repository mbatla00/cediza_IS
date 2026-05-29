from mysql.connector import Error
from .database import Database
from src.modelo.vo import Paciente, PacPri, PacPub


class PacienteDAO:

    @staticmethod
    def get_all():
        db = Database()
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
                row_raw = Database.row_to_dict(cursor, raw_row)
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
        db = Database()
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
        db = Database()
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
        db = Database()
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


class PacPubDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Pac_pub WHERE nombreUsuario = ?", (nombreUsuario,))
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return PacPub(**row) if row else None
        except Error as e:
            print(f"Error en PacPubDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pac_pub):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = "INSERT INTO Pac_pub (nombreUsuario, Dias_ingresado) VALUES (?, ?)"
            cursor.execute(sql, (pac_pub.nombreUsuario, pac_pub.dias_ingresado))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPubDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_dias(nombreUsuario, dias_ingresado):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Pac_pub SET Dias_ingresado = ? WHERE nombreUsuario = ?",
                (dias_ingresado, nombreUsuario)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPubDAO.update_dias: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


class PacPriDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Pac_pri WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return PacPri(**row) if row else None
        except Error as e:
            print(f"Error en PacPriDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pac_pri):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Pac_pri (nombreUsuario, IVA, cuenta, horas)
                     VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (
                pac_pri.nombreUsuario,
                pac_pri.iva,
                pac_pri.cuenta,
                pac_pri.horas
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPriDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update(pac_pri):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Pac_pri
                     SET IVA = ?, cuenta = ?, horas = ?
                     WHERE nombreUsuario = ?"""
            cursor.execute(sql, (
                pac_pri.iva,
                pac_pri.cuenta,
                pac_pri.horas,
                pac_pri.nombreUsuario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en PacPriDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()