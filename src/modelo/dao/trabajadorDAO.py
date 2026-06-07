from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Trabajador, Auxiliar, Coordinador, Especialista
from mysql.connector import Error

"""
Tabla para los trabajadores
subtipo de usuarios
"""

GET_ALL = "SELECT * FROM Trabajadores"
GET_BY_USER = "SELECT * FROM Trabajadores WHERE nombreUsuario = ?"
CREATE = "INSERT INTO Trabajadores (nombreUsuario, Tipo) VALUES (?, ?)"
DELETE = "DELETE FROM Trabajadores WHERE nombreUsuario = ?"


class TrabajadorDAO:

    @staticmethod
    def _build_vo(row: dict):
        """Construye el VO correcto a partir de un dict con claves en minúscula."""
        tipo = row.get('tipo')
        common = dict(
            nombreUsuario=row.get('nombreusuario'),
            Nombre=row.get('nombre'),
            DNI=row.get('dni'),
            password=row.get('password'),
            email=row.get('email'),
            fechaNacimiento=row.get('fechanacimiento'),
            telefono=row.get('telefono'),
            activo=row.get('activo'),
        )
        if tipo == 'auxiliar':
            return Auxiliar(**common, Horario=row.get('horario'))
        elif tipo == 'coordinador':
            return Coordinador(**common, infoInteres=row.get('infointeres'))
        elif tipo == 'especialista':
            return Especialista(
                **common,
                Especialidad=row.get('especialidad'),
                Horario=row.get('horario')
            )
        else:
            return None  # tipo desconocido, se ignora

    @staticmethod
    def get_all():
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.*, u.Nombre, u.DNI, u.email, u.fechaNacimiento, u.telefono, u.activo
                FROM Trabajadores t
                JOIN Usuarios u ON t.nombreUsuario = u.nombreUsuario
                WHERE u.activo = 1
            """)
            raw_rows = cursor.fetchall()

            trabajadores = []
            for raw_row in raw_rows:
                row_raw = Database.row_to_dict(cursor, raw_row)
                if not row_raw:
                    continue
                row = {k.lower(): v for k, v in row_raw.items()}
                vo = TrabajadorDAO._build_vo(row)
                if vo:
                    trabajadores.append(vo)

            return trabajadores
        except Exception as e:
            print(f"Error crítico en TrabajadorDAO.get_all: {e}")
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
                SELECT t.*, u.Nombre, u.DNI, u.email, u.fechaNacimiento, u.telefono, u.activo
                FROM Trabajadores t
                JOIN Usuarios u ON t.nombreUsuario = u.nombreUsuario
                WHERE t.nombreUsuario = ?
            """, (nombreUsuario,))
            raw_row = cursor.fetchone()

            if raw_row:
                row_raw = Database.row_to_dict(cursor, raw_row)
                if not row_raw:
                    return None
                row = {k.lower(): v for k, v in row_raw.items()}
                return TrabajadorDAO._build_vo(row)
            return None
        except Exception as e:
            print(f"Error crítico en TrabajadorDAO.get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(trabajador):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (trabajador.nombreUsuario, trabajador.tipo))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en TrabajadorDAO.create: {e}")
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
            cursor.execute(DELETE, (nombreUsuario,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en TrabajadorDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()