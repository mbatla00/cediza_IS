from mysql.connector import Error
from app.dao.database import Database
from app.factories.usuario_factory import UsuarioFactory
import unicodedata
import re


class UsuarioDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT u.*, p.Tipo as TipoPaciente, t.Tipo as TipoTrabajador
                FROM Usuarios u
                LEFT JOIN Pacientes p ON u.nombreUsuario = p.nombreUsuario
                LEFT JOIN Trabajadores t ON u.nombreUsuario = t.nombreUsuario
                WHERE u.nombreUsuario = ?
            """, (nombreUsuario,))
            row = Database.row_to_dict(cursor, cursor.fetchone())
            if row:
                if row.get('TipoPaciente'):
                    row['Tipo'] = row['TipoPaciente']
                elif row.get('TipoTrabajador'):
                    row['Tipo'] = row['TipoTrabajador']
            return UsuarioFactory.crear(row) if row else None
        except Error as e:
            print(f"Error en get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_email(email):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Usuarios WHERE email = ?",
                (email,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return UsuarioFactory.crear(row) if row else None
        except Error as e:
            print(f"Error en get_by_email: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_dni(dni):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Usuarios WHERE DNI = ?",
                (dni,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return UsuarioFactory.crear(row) if row else None
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            email = getattr(usuario, 'email', None)
            sql = """INSERT INTO Usuarios (nombreUsuario, Nombre, email, DNI, Rol, password)
            VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                usuario.nombreUsuario,
                usuario.nombre,
                email,
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Usuarios
            SET Nombre = ?, email = ?, DNI = ?, password = ?
            WHERE nombreUsuario = ?"""
            cursor.execute(sql, (
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Usuarios SET activo = 0 WHERE nombreUsuario = ?",
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