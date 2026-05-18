from mysql.connector import Error
from app.dao.database import Database
from app.models.familiar import Familiar
from app.models.comentarios import Comentario
from app.models.sesion import Sesion
 
 
class FamiliarDAO:
    #Operaciones sobre la tabla Familiares
 
    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        #Devuelve todos los familiares de un paciente.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []
 
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """SELECT Nombre, Paciente, Relación AS Relacion, Telefono 
                     FROM Familiares 
                     WHERE Paciente = %s"""
                     
            cursor.execute(sql, (nombreUsuario_paciente,))  #cambiar si se quita la tilde en el database!!
            return [Familiar(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en FamiliarDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()
 
    @staticmethod
    def create(familiar):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Familiares (Nombre, Paciente, Relación, Telefono)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (
                familiar.nombre,
                familiar.paciente,
                familiar.relacion,
                familiar.telefono
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FamiliarDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
 
    @staticmethod
    def delete(nombre, nombreUsuario_paciente):
        #Elimina un familiar por nombre y paciente al que pertenece.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Familiares WHERE Nombre = %s AND Paciente = %s",
                (nombre, nombreUsuario_paciente)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FamiliarDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
 
 
class ComentarioDAO:
    #Operaciones sobre la tabla comentarios.
 
    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        """Devuelve todos los comentarios de un paciente."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []
 
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Paciente = %s ORDER BY dia DESC",
                (nombreUsuario_paciente,)
            )
            return [Comentario(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en ComentarioDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()
 
    @staticmethod
    def get_by_trabajador(nombreUsuario_trabajador):
        """Devuelve todos los comentarios escritos por un trabajador."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []
 
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Auxiliar = %s ORDER BY dia DESC",
                (nombreUsuario_trabajador,)
            )
            return [Comentario(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en ComentarioDAO.get_by_trabajador: {e}")
            return []
        finally:
            cursor.close()
 
    @staticmethod
    def create(comentario):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO comentarios (Auxiliar, Paciente, dia, nota)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (
                comentario.auxiliar,
                comentario.paciente,
                comentario.dia,
                comentario.nota
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
 
    @staticmethod
    def delete(auxiliar, paciente, dia):
        """Elimina un comentario concreto por su clave compuesta."""
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM comentarios WHERE Auxiliar = %s AND Paciente = %s AND dia = %s",
                (auxiliar, paciente, dia)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en ComentarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
 
 
class SesionDAO:
    #Operaciones sobre la tabla Sesion.
 
    @staticmethod
    def get_by_id(idSesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None
 
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE idSesion = %s",
                (idSesion,)
            )
            row = cursor.fetchone()
            return Sesion(**row) if row else None
        except Error as e:
            print(f"Error en SesionDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()
 
    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        #Devuelve todas las sesiones de un paciente ordenadas por fecha.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []
 
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE Paciente = %s ORDER BY Fecha ASC",
                (nombreUsuario_paciente,)
            )
            return [Sesion(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en SesionDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()
 
    @staticmethod
    def get_by_especialista(nombreUsuario_especialista):
        #Devuelve todas las sesiones de un especialista ordenadas por fecha.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []
 
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM Sesion WHERE Especialista = %s ORDER BY Fecha ASC",
                (nombreUsuario_especialista,)
            )
            return [Sesion(**row) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error en SesionDAO.get_by_especialista: {e}")
            return []
        finally:
            cursor.close()
 
    @staticmethod
    def create(sesion):
        #Inserta una nueva sesión y devuelve su idSesion generado.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None
 
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Sesion (Paciente, Especialista, comentarios, Fecha)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                sesion.fecha
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error en SesionDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
 
    @staticmethod
    def update(sesion):
        #Actualiza los datos de una sesión existente.
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            sql = """UPDATE Sesion
                     SET Paciente = %s, Especialista = %s, comentarios = %s, Fecha = %s
                     WHERE idSesion = %s"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                sesion.fecha,
                sesion.idSesion
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en SesionDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
 
    @staticmethod
    def delete(idSesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False
 
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Sesion WHERE idSesion = %s",
                (idSesion,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en SesionDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()