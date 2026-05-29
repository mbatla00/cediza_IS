from mysql.connector import Error
from .database import Database
from src.modelo.vo import Familiar, Comentario, Sesion
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
                "SELECT id, Auxiliar, Paciente, dia, hora, nota FROM comentarios WHERE Paciente = ? ORDER BY dia DESC, hora DESC",
                (nombreUsuario_paciente,)
            )
            rows = cursor.fetchall()
            
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'hora': row[4],
                    'nota': row[5]
                }
                comentarios.append(Comentario(**row_dict))
            return comentarios
        except Exception as e:
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
                "SELECT id, Auxiliar, Paciente, dia, hora, nota FROM comentarios WHERE Auxiliar = ? ORDER BY dia DESC, hora DESC",
                (nombreUsuario_trabajador,)
            )
            rows = cursor.fetchall()
            
            comentarios = []
            for row in rows:
                row_dict = {
                    'id': row[0],
                    'Auxiliar': row[1],
                    'Paciente': row[2],
                    'dia': row[3],
                    'hora': row[4],
                    'nota': row[5]
                }
                comentarios.append(Comentario(**row_dict))
            return comentarios
        except Exception as e:
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
            dia_str = str(comentario.dia) if comentario.dia else None
            hora_str = str(comentario.hora) if comentario.hora else None
            
            sql = """INSERT INTO comentarios (Auxiliar, Paciente, dia, hora, nota)
                     VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                comentario.auxiliar,
                comentario.paciente,
                dia_str,
                hora_str,
                comentario.nota
            ))
            conn.commit()
            return True
        except Exception as e:
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
                "SELECT * FROM Sesion WHERE idSesion = ?",
                (idSesion,)
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0].split('.')[-1] for col in cursor.description]
                row_dict = dict(zip(columns, row))
                
                # Convertir fecha
                fecha_val = row_dict.get('Fecha')
                if fecha_val and isinstance(fecha_val, str):
                    fecha_val = datetime.strptime(fecha_val, '%Y-%m-%d').date()
                
                # Convertir hora
                hora_val = row_dict.get('hora')
                if hora_val and isinstance(hora_val, str):
                    try:
                        hora_val = datetime.strptime(hora_val, '%H:%M:%S').time()
                    except ValueError:
                        hora_val = datetime.strptime(hora_val, '%H:%M').time()
                
                sesion = Sesion(
                    idSesion=row_dict.get('idSesion'),
                    Paciente=row_dict.get('Paciente'),
                    Especialista=row_dict.get('Especialista'),
                    comentarios=row_dict.get('comentarios'),
                    Fecha=fecha_val,
                    Hora=hora_val
                )
                return sesion
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
                "SELECT * FROM Sesion WHERE Paciente = ? ORDER BY Fecha ASC",
                (nombreUsuario_paciente,)
            )
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            sesiones = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                
                # Convertir fecha de string a date
                fecha_val = row_dict.get('Fecha')
                if fecha_val and isinstance(fecha_val, str):
                    fecha_val = datetime.strptime(fecha_val, '%Y-%m-%d').date()
                
                # Convertir hora de string a time
                hora_val = row_dict.get('hora')
                if hora_val and isinstance(hora_val, str):
                    try:
                        hora_val = datetime.strptime(hora_val, '%H:%M:%S').time()
                    except ValueError:
                        hora_val = datetime.strptime(hora_val, '%H:%M').time()
                
                sesion = Sesion(
                    idSesion=row_dict.get('idSesion'),
                    Paciente=row_dict.get('Paciente'),
                    Especialista=row_dict.get('Especialista'),
                    comentarios=row_dict.get('comentarios'),
                    Fecha=fecha_val,
                    Hora=hora_val
                )
                sesiones.append(sesion)
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
                "SELECT * FROM Sesion WHERE Especialista = ? ORDER BY Fecha ASC",
                (nombreUsuario_especialista,)
            )
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            sesiones = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                
                # Convertir fecha de string a date
                fecha_val = row_dict.get('Fecha')
                if fecha_val and isinstance(fecha_val, str):
                    fecha_val = datetime.strptime(fecha_val, '%Y-%m-%d').date()
                
                # Convertir hora de string a time
                hora_val = row_dict.get('hora')
                if hora_val and isinstance(hora_val, str):
                    try:
                        hora_val = datetime.strptime(hora_val, '%H:%M:%S').time()
                    except ValueError:
                        hora_val = datetime.strptime(hora_val, '%H:%M').time()
                
                sesion = Sesion(
                    idSesion=row_dict.get('idSesion'),
                    Paciente=row_dict.get('Paciente'),
                    Especialista=row_dict.get('Especialista'),
                    comentarios=row_dict.get('comentarios'),
                    Fecha=fecha_val,
                    Hora=hora_val
                )
                sesiones.append(sesion)
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