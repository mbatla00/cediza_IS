from mysql.connector import Error
from app.dao.database import Database
from app.models.familiar import Familiar
from app.models.comentarios import Comentario
from app.models.sesion import Sesion
from datetime import datetime


class FamiliarDAO:

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Familiares WHERE Paciente = ?",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Familiar(**row) for row in rows]
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
            sql = """INSERT INTO Familiares (Nombre, Paciente, Relacion, Telefono)
                     VALUES (?, ?, ?, ?)"""
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Familiares WHERE Nombre = ? AND Paciente = ?",
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

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Paciente = ? ORDER BY dia DESC",
                (nombreUsuario_paciente,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Comentario(**row) for row in rows]
        except Error as e:
            print(f"Error en ComentarioDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_trabajador(nombreUsuario_trabajador):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM comentarios WHERE Auxiliar = ? ORDER BY dia DESC",
                (nombreUsuario_trabajador,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Comentario(**row) for row in rows]
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
                     VALUES (?, ?, CURDATE(), ?)"""
            cursor.execute(sql, (
                comentario.auxiliar,
                comentario.paciente,
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
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM comentarios WHERE Auxiliar = ? AND Paciente = ? AND dia = ?",
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

    @staticmethod
    def get_by_id(idSesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT idSesion, Paciente, Especialista, comentarios, Fecha, Hora FROM Sesion WHERE idSesion = ?",
                (idSesion,)
            )
            row = cursor.fetchone()
            if row:
                row_dict = {
                    'idSesion': row[0],
                    'Paciente': row[1],
                    'Especialista': row[2],
                    'comentarios': row[3],
                    'Fecha': row[4],
                    'Hora': row[5]
                }
                # Convertir fecha de string a date si es necesario
                if row_dict['Fecha'] and isinstance(row_dict['Fecha'], str):
                    try:
                        row_dict['Fecha'] = datetime.strptime(row_dict['Fecha'], '%Y-%m-%d').date()
                    except:
                        pass
                return Sesion(**row_dict)
            return None
        except Error as e:
            print(f"Error en SesionDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_paciente(nombreUsuario_paciente):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT idSesion, Paciente, Especialista, comentarios, Fecha, Hora FROM Sesion WHERE Paciente = ? ORDER BY Fecha ASC",
                (nombreUsuario_paciente,)
            )
            rows = cursor.fetchall()
            
            sesiones = []
            for row in rows:
                row_dict = {
                    'idSesion': row[0],
                    'Paciente': row[1],
                    'Especialista': row[2],
                    'comentarios': row[3],
                    'Fecha': row[4],
                    'Hora': row[5]
                }
                # Convertir fecha de string a date si es necesario
                if row_dict['Fecha'] and isinstance(row_dict['Fecha'], str):
                    try:
                        row_dict['Fecha'] = datetime.strptime(row_dict['Fecha'], '%Y-%m-%d').date()
                    except:
                        pass
                sesiones.append(Sesion(**row_dict))
            return sesiones
        except Exception as e:
            print(f"Error en SesionDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_especialista(nombreUsuario_especialista):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT idSesion, Paciente, Especialista, comentarios, Fecha, Hora FROM Sesion WHERE Especialista = ? ORDER BY Fecha ASC",
                (nombreUsuario_especialista,)
            )
            rows = cursor.fetchall()
            
            sesiones = []
            for row in rows:
                row_dict = {
                    'idSesion': row[0],
                    'Paciente': row[1],
                    'Especialista': row[2],
                    'comentarios': row[3],
                    'Fecha': row[4],
                    'Hora': row[5]
                }
                # Convertir fecha de string a date si es necesario
                if row_dict['Fecha'] and isinstance(row_dict['Fecha'], str):
                    try:
                        row_dict['Fecha'] = datetime.strptime(row_dict['Fecha'], '%Y-%m-%d').date()
                    except:
                        pass
                sesiones.append(Sesion(**row_dict))
            return sesiones
        except Exception as e:
            print(f"Error en SesionDAO.get_by_especialista: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(sesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            # Convertir fecha y hora a string para JDBC
            fecha_str = str(sesion.fecha) if sesion.fecha else None
            hora_str = str(sesion.hora) if sesion.hora else None
            
            sql = """INSERT INTO Sesion (Paciente, Especialista, comentarios, Fecha, Hora)
                     VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                fecha_str,
                hora_str
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en SesionDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(sesion):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Convertir fecha y hora a string para JDBC
            fecha_str = str(sesion.fecha) if sesion.fecha else None
            hora_str = str(sesion.hora) if sesion.hora else None
            
            sql = """UPDATE Sesion
                     SET Paciente = ?, Especialista = ?, comentarios = ?, Fecha = ?, Hora = ?
                     WHERE idSesion = ?"""
            cursor.execute(sql, (
                sesion.paciente,
                sesion.especialista,
                sesion.comentarios,
                fecha_str,
                hora_str,
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
                "DELETE FROM Sesion WHERE idSesion = ?",
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