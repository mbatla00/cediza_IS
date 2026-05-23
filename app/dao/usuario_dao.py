from mysql.connector import Error
from app.dao.database import Database
from app.factories.usuario_factory import UsuarioFactory
import unicodedata
import re


class UsuarioDAO:

    # -------------------------------------------------------------
    # Buscar por nombre de usuario (PK)
    # -------------------------------------------------------------
    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        """Devuelve un objeto Usuario o None"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT u.*, p.Tipo as TipoPaciente, t.Tipo as TipoTrabajador
                FROM Usuarios u
                LEFT JOIN Pacientes p ON u.nombreUsuario = p.nombreUsuario
                LEFT JOIN Trabajadores t ON u.nombreUsuario = t.nombreUsuario
                WHERE u.nombreUsuario = %s
            """, (nombreUsuario,))
            row = cursor.fetchone()
            
            if row:
                # Unificar el campo Tipo
                if row.get('TipoPaciente'):
                    row['Tipo'] = row['TipoPaciente']
                elif row.get('TipoTrabajador'):
                    row['Tipo'] = row['TipoTrabajador']
                
                # Crear el objeto y parchear el email
                usuario_obj = UsuarioFactory.crear(row)
                if usuario_obj and 'email' in row:
                    usuario_obj.email = row.get('email')
                
                return usuario_obj
            return None
            
        except Error as e:
            print(f"Error en get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    # -------------------------------------------------------------
    # Buscar por email
    # -------------------------------------------------------------
    @staticmethod
    def get_by_email(email):
        """Busca un usuario por email. Devuelve Usuario o None"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Usuarios WHERE email = %s",
                (email,)
            )
            row = cursor.fetchone()
            
            if row:
                usuario_obj = UsuarioFactory.crear(row)
                if usuario_obj and 'email' in row:
                    usuario_obj.email = row.get('email')
                return usuario_obj
                
            return None
        except Error as e:
            print(f"Error en get_by_email: {e}")
            return None
        finally:
            cursor.close()

    # -------------------------------------------------------------
    # Buscar por DNI
    # -------------------------------------------------------------
    @staticmethod
    def get_by_dni(dni):
        """Busca un usuario por DNI. Devuelve Usuario o None"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Usuarios WHERE DNI = %s",
                (dni,)
            )
            row = cursor.fetchone()
            
            if row:
                usuario_obj = UsuarioFactory.crear(row)
                if usuario_obj and 'email' in row:
                    usuario_obj.email = row.get('email')
                return usuario_obj
                
            return None
        except Error as e:
            print(f"Error en get_by_dni: {e}")
            return None
        finally:
            cursor.close()

    # -------------------------------------------------------------
    # Validar DNI español
    # -------------------------------------------------------------
    @staticmethod
    def validar_dni(dni):
        """
        Valida formato y letra de un DNI español.
        Devuelve True si es válido, False si no.
        """
        if not re.match(r'^\d{8}[A-Za-z]$', dni):
            return False

        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:-1])
        letra = dni[-1].upper()
        return letras[numero % 23] == letra

    # -------------------------------------------------------------
    # Generar nombre de usuario sin acentos ni espacios
    # -------------------------------------------------------------
    @staticmethod
    def generar_nombre_usuario(nombre, apellido1, apellido2=""):
        """
        Genera nombreUsuario = nombre + apellido1 [+ apellido2].
        Sin acentos, sin espacios, en minúsculas.
        Si ya existe, añade número al final.
        """
        base = f"{nombre}{apellido1}{apellido2}".lower()
        base = unicodedata.normalize('NFKD', base).encode('ASCII', 'ignore').decode('ASCII')
        base = ''.join(c for c in base if c.isalnum())

        nombre_final = base
        contador = 1
        while UsuarioDAO.get_by_nombreUsuario(nombre_final) is not None:
            nombre_final = f"{base}{contador}"
            contador += 1

        return nombre_final

    # -------------------------------------------------------------
    # Crear usuario
    # -------------------------------------------------------------
    @staticmethod
    def create(usuario):
        """Inserta un nuevo usuario. Devuelve True si éxito, False si fallo"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            email = getattr(usuario, 'email', None)
            sql = """INSERT INTO Usuarios (nombreUsuario, Nombre, email, DNI, Rol, password)
            VALUES (%s, %s, %s, %s, %s, %s)"""
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

    # -------------------------------------------------------------
    # Actualizar usuario
    # -------------------------------------------------------------
    @staticmethod
    def update(usuario):
        """Actualiza nombre, email, DNI y contraseña"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            sql = """UPDATE Usuarios
            SET Nombre = %s, email = %s, DNI = %s, password = %s
            WHERE nombreUsuario = %s"""
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

    # -------------------------------------------------------------
    # Eliminar usuario (borrado lógico)
    # -------------------------------------------------------------
    @staticmethod
    def delete(nombreUsuario):
        """Marca un usuario como inactivo"""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Usuarios SET activo = 0 WHERE nombreUsuario = %s",
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