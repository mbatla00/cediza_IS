from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Sesion

GET_BY_ID = "SELECT * FROM Sesion WHERE idSesion = ?"
GET_BY_PACIENTE = "SELECT * FROM Sesion WHERE Paciente = ? ORDER BY Fecha ASC"
GET_BY_ESPECIALISTA = "SELECT * FROM Sesion WHERE Especialista = ? ORDER BY Fecha ASC"
CREATE = """INSERT INTO Sesion (Paciente, Especialista, comentarios, Fecha, Hora)
                     VALUES (?, ?, ?, ?, ?)"""
UPDATE = """UPDATE Sesion
                     SET Paciente = ?, Especialista = ?, comentarios = ?, Fecha = ?, Hora = ?
                     WHERE idSesion = ?"""
DELETE = "DELETE FROM Sesion WHERE idSesion = ?"

class SesionDAO:

    @staticmethod
    def get_by_id(idSesion):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ID,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_PACIENTE,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ESPECIALISTA,
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            fecha_str = str(sesion.fecha) if sesion.fecha else None
            hora_str = str(sesion.hora) if sesion.hora else None
            
            cursor.execute(CREATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            fecha_str = str(sesion.fecha) if sesion.fecha else None
            hora_str = str(sesion.hora) if sesion.hora else None
            
            cursor.execute(UPDATE, (
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
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
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