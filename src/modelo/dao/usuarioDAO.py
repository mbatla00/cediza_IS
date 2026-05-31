from src.modelo.conexion.Conexion import Conexion
Database = Conexion
from src.modelo.factories import UsuarioFactory
import unicodedata
import re
from mysql.connector import Error

GET_BY_USER = """
                SELECT u.*, p.Tipo as TipoPaciente, t.Tipo as TipoTrabajador
                FROM Usuarios u
                LEFT JOIN Pacientes p ON u.nombreUsuario = p.nombreUsuario
                LEFT JOIN Trabajadores t ON u.nombreUsuario = t.nombreUsuario
                WHERE u.nombreUsuario = ?
            """
GET_BY_EMAIL = "SELECT * FROM Usuarios WHERE email = ?"
GET_BY_DNI = "SELECT * FROM Usuarios WHERE DNI = ?"
CREATE = """INSERT INTO Usuarios (nombreUsuario, Nombre, email, fechaNacimiento, DNI, Rol, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)"""
UPDATE = """UPDATE Usuarios
            SET Nombre = ?, email = ?, DNI = ?, password = ?
            WHERE nombreUsuario = ?"""
DELETE = "UPDATE Usuarios SET activo = 0 WHERE nombreUsuario = ?"
GET_ALL = """
                SELECT u.*, p.Tipo as TipoPaciente, t.Tipo as TipoTrabajador
                FROM Usuarios u
                LEFT JOIN Pacientes p ON u.nombreUsuario = p.nombreUsuario
                LEFT JOIN Trabajadores t ON u.nombreUsuario = t.nombreUsuario
            """

class UsuarioDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(GET_BY_USER, (nombreUsuario,))

            row = Conexion.row_to_dict(cursor, cursor.fetchone())

            if row:
                if row.get('TipoPaciente'):
                    row['Tipo'] = row['TipoPaciente']
                elif row.get('TipoTrabajador'):
                    row['Tipo'] = row['TipoTrabajador']
                
                usuario_obj = UsuarioFactory.crear(row)
                #if usuario_obj and 'email' in row:
                #    usuario_obj.email = row.get('email')
                
                return usuario_obj
            return None
            
        except Error as e:
            print(f"Error en get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_email(email):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_EMAIL,
                (email,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            if row:
                usuario_obj = UsuarioFactory.crear(row)
                if usuario_obj and ('email' in row or 'Email' in row):
                    usuario_obj.email = row.get('email') or row.get('Email')
                return usuario_obj
                
            return None
        except Error as e:
            print(f"Error en get_by_email: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_dni(dni):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_DNI,
                (dni,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            if row:
                usuario_obj = UsuarioFactory.crear(row)
                if usuario_obj and ('email' in row or 'Email' in row):
                    usuario_obj.email = row.get('email') or row.get('Email')
                return usuario_obj
                
            return None
        except Error as e:
            print(f"Error en get_by_dni: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def validar_dni(dni):
        if not re.match(r'^\d{8}[A-Za-z]$', dni):
            return False
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:-1])
        letra = dni[-1].upper()
        return letras[numero % 23] == letra

    @staticmethod
    def generar_nombre_usuario(nombre, apellido1, apellido2=""):
        base = f"{nombre}{apellido1}{apellido2}".lower()
        base = unicodedata.normalize('NFKD', base).encode('ASCII', 'ignore').decode('ASCII')
        base = ''.join(c for c in base if c.isalnum())

        nombre_final = base
        contador = 1
        while UsuarioDAO.get_by_nombreUsuario(nombre_final) is not None:
            nombre_final = f"{base}{contador}"
            contador += 1
        return nombre_final

    @staticmethod
    def create(usuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            email = getattr(usuario, 'email', None)

            cursor.execute(CREATE, (
                usuario.nombreUsuario,
                usuario.nombre,
                email,
                usuario.fechaNacimiento,
                usuario.dni,
                usuario.rol,
                usuario.password
            ))
            conn.commit()
            return True
        except Error as e:
            print(f'Error en create usuario: {e}')
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update(usuario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(UPDATE, (
                usuario.nombre,
                usuario.email,
                usuario.dni,
                usuario.password,
                usuario.nombreUsuario
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en update usuario: {e}")
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
            print(f"Error en delete usuario: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        """Devuelve una lista de todos los objetos Usuario válidos en el sistema."""
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(GET_ALL)
            raw_rows = cursor.fetchall()
            
            usuarios = []
            for raw_row in raw_rows:
                row_raw = Database.row_to_dict(cursor, raw_row)
                if not row_raw:
                    continue
                
                row = {}
                for k, v in row_raw.items():
                    row[k] = v
                    row[k.lower()] = v
                
                if 'nombreusuario' in row: row['nombreUsuario'] = row['nombreusuario']
                if 'tipopaciente' in row: row['TipoPaciente'] = row['tipopaciente']
                if 'tipotrabajador' in row: row['TipoTrabajador'] = row['tipotrabajador']
                if 'fechanacimiento' in row: row['fechaNacimiento'] = row['fechanacimiento']

                val_activo = row.get('activo')
                if val_activo is None:
                    val_activo = row.get('Activo')
                
                if val_activo is True or val_activo == 1 or str(val_activo).lower() in ('1', 'true'):
                    estado_corregido = 1
                else:
                    estado_corregido = 0
                
                row['activo'] = estado_corregido
                row['Activo'] = estado_corregido

                rol = (row.get('Rol') or row.get('rol') or '').lower()
                row['Rol'] = rol
                
                if rol == 'paciente':
                    tipo_val = row.get('TipoPaciente') or row.get('tipopaciente') or ''
                    row['Tipo'] = tipo_val
                    row['tipo'] = tipo_val
                elif rol == 'trabajador':
                    tipo_val = row.get('TipoTrabajador') or row.get('tipotrabajador') or ''
                    row['Tipo'] = tipo_val
                    row['tipo'] = tipo_val
                else:
                    row['Tipo'] = ''
                    row['tipo'] = ''

                try:
                    usuario_objeto = UsuarioFactory.crear(row)
                    if usuario_objeto:
                        usuario_objeto.activo = estado_corregido
                        usuarios.append(usuario_objeto)
                except Exception as e:
                    print(f"Alerta: Saltando usuario '{row.get('nombreUsuario') or row.get('nombreusuario')}'. Motivo: {e}")
                    continue
            
            return usuarios
            
        except Exception as e:
            print(f"Error crítico en database al listar usuarios: {e}")
            return []
        finally:
            cursor.close()