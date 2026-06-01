from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.vo import Trabajador, Auxiliar, Coordinador, Especialista
from mysql.connector import Error

GET_ALL = "SELECT * FROM Trabajadores"
GET_BY_USER = "SELECT * FROM Trabajadores WHERE nombreUsuario = ?"
CREATE = "INSERT INTO Trabajadores (nombreUsuario, Tipo) VALUES (?, ?)"
DELETE = "DELETE FROM Trabajadores WHERE nombreUsuario = ?"


class TrabajadorDAO:

    @staticmethod
    def get_all():
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.*, u.Nombre, u.DNI, u.email, u.activo 
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
                
                tipo = row.get('tipo')
                
                if tipo == 'auxiliar':
                    trabajador_obj = Auxiliar(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Horario=row.get('horario')
                    )
                elif tipo == 'coordinador':
                    trabajador_obj = Coordinador(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        infoInteres=row.get('infointeres')
                    )
                elif tipo == 'especialista':
                    trabajador_obj = Especialista(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Especialidad=row.get('especialidad'),
                        Horario=row.get('horario')
                    )
                else:
                    trabajador_obj = Trabajador(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Tipo=tipo
                    )
                
                trabajadores.append(trabajador_obj)
                
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
                SELECT t.*, u.Nombre, u.DNI, u.email, u.activo 
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
                
                tipo = row.get('tipo')
                
                if tipo == 'auxiliar':
                    return Auxiliar(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Horario=row.get('horario')
                    )
                elif tipo == 'coordinador':
                    return Coordinador(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        infoInteres=row.get('infointeres')
                    )
                elif tipo == 'especialista':
                    return Especialista(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Especialidad=row.get('especialidad'),
                        Horario=row.get('horario')
                    )
                else:
                    return Trabajador(
                        nombreUsuario=row.get('nombreusuario'),
                        Nombre=row.get('nombre'),
                        DNI=row.get('dni'),
                        password=None,
                        Tipo=tipo
                    )
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
            cursor.execute(
                DELETE,
                (nombreUsuario,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en TrabajadorDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()


