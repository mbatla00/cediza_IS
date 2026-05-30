from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Cuestionario

GET_ALL = "SELECT * FROM Cuestionarios"
GET_BY_ID = "SELECT * FROM Cuestionarios WHERE idCuestionario = ?"
CREATE = """INSERT INTO Cuestionarios (titulo, tipo, fechaAsignacion)
                     VALUES (?, ?, ?)"""
UPDATE = """UPDATE Cuestionarios
                     SET titulo = ?, tipo = ?, fechaAsignacion = ?
                     WHERE idCuestionario = ?"""
DELETE = "DELETE FROM Cuestionarios WHERE idCuestionario = ?"


class CuestionarioDAO:

    @staticmethod
    def get_all():
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(GET_ALL)
            rows = cursor.fetchall()
            columns = [col[0].split('.')[-1] for col in cursor.description]
            
            cuestionarios = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                cuestionario = Cuestionario(
                    idCuestionario=row_dict.get('idCuestionario'),
                    titulo=row_dict.get('titulo'),
                    tipo=row_dict.get('tipo'),
                    fechaAsignacion=row_dict.get('fechaAsignacion')
                )
                cuestionarios.append(cuestionario)
            return cuestionarios
        except Exception as e:
            print(f"Error en CuestionarioDAO.get_all: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(idCuestionario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ID,
                (idCuestionario,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0].split('.')[-1] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            return Cuestionario(
                idCuestionario=row_dict.get('idCuestionario'),
                titulo=row_dict.get('titulo'),
                tipo=row_dict.get('tipo'),
                fechaAsignacion=row_dict.get('fechaAsignacion')
            )
        except Exception as e:
            print(f"Error en CuestionarioDAO.get_by_id: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(cuestionario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(CREATE, (
                cuestionario.titulo,
                cuestionario.tipo,
                cuestionario.fechaAsignacion
            ))
            conn.commit()
            return True  # JDBC no tiene lastrowid
        except Exception as e:
            print(f"Error en CuestionarioDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(cuestionario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(UPDATE, (
                cuestionario.titulo,
                cuestionario.tipo,
                cuestionario.fechaAsignacion,
                cuestionario.idCuestionario
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en CuestionarioDAO.update: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(idCuestionario):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (idCuestionario,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en CuestionarioDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()



