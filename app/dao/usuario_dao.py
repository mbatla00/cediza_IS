from mysql.connector import Error
from app.dao.database import Database
from app.factories.usuario_factory import UsuarioFactory

class UsuarioDAO:

    @staticmethod
    def get_by_nombreUsuario(nombreUsuario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT u.*, p.Tipo
                FROM Usuarios u
                LEFT JOIN Pacientes p ON u.nombreUsuario = p.nombreUsuario
                LEFT JOIN Trabajadores t ON u.nombreUsuario = t.nombreUsuario
            WHERE u.nombreUsuario = %s
            """, (nombreUsuario,))
            row = cursor.fetchone()
            return UsuarioFactory.crear(row) if row else None
        except Error as e:
            print(f"Error en get_by_nombreUsuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_dni(dni):
        #Busca un usuario por DNI
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Usuarios WHERE DNI = %s",
                (dni, )
            )
            row = cursor.fetchone()
            return UsuarioFactory.crear(row) if row else None
        except Error as e:
            print(f"Error en get_by_dni: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(usuario):
        #Inserta un nuevo usuario, devuelve True si tuvo éxito
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Usuarios (nombreUsuario, Nombre, DNI, Rol, contraseña)
                VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                usuario.nombreUsuario,
                usuario.nombre,
                usuario.dni,
                usuario.rol,
                usuario.contraseña
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
        #actualiza nombre, DNI y contraseña de un usuario
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        try:
            sql = """UPDATE Usuarios
                SET Nombre = %s, DNI = %s, contraseña = %s 
                WHERE nombreUsuario = %s"""
            cursor.execute(sql, (
                usuario.nombre,
                usuario.dni,
                usuario.contraseña,
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
        #Elimina un usuario por su nombre de usuario
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Usuarios WHERE nombreUsuario = %s",
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
        