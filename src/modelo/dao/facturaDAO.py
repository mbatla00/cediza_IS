from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo import Factura

GET_BY_CODIGO = "SELECT * FROM Factura WHERE codigoFactura = ?"
GET_BY_PACIENTE = """SELECT * FROM Factura
                   WHERE Paciente = ? ORDER BY fechaEmision DESC"""
GET_BY_ADMIN = """SELECT * FROM Factura
                   WHERE Administrador = ? ORDER BY fechaEmision DESC"""
CREATE = """INSERT INTO Factura
                     (codigoFactura, Paciente, Administrador, fechaEmision, importeTotal, estadoPago)
                     VALUES (?, ?, ?, ?, ?, ?)"""
UPDATE_ESTADO = "UPDATE Factura SET estadoPago = ? WHERE codigoFactura = ?"
UPDATE_IMPORTE = "UPDATE Factura SET importeTotal = ? WHERE codigoFactura = ?"
DELETE = "DELETE FROM Factura WHERE codigoFactura = ?"

class FacturaDAO:

    @staticmethod
    def get_by_codigo(codigoFactura):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_CODIGO,
                (codigoFactura,)
            )
            row = Database.row_to_dict(cursor, cursor.fetchone())
            return Factura(**row) if row else None
        except Error as e:
            print(f"Error en FacturaDAO.get_by_codigo: {e}")
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
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Factura(**row) for row in rows]
        except Error as e:
            print(f"Error en FacturaDAO.get_by_paciente: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_administrador(nombreUsuario_admin):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            cursor.execute(
                GET_BY_ADMIN,
                (nombreUsuario_admin,)
            )
            rows = Database.rows_to_dict(cursor, cursor.fetchall())
            return [Factura(**row) for row in rows]
        except Error as e:
            print(f"Error en FacturaDAO.get_by_administrador: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(factura):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Convertir fecha para JDBC
            fecha_emision = factura.fechaEmision
            if isinstance(fecha_emision, date):
                import time
                SQLDate = jpype.JClass("java.sql.Date")
                timestamp = int(time.mktime(fecha_emision.timetuple()) * 1000)
                fecha_emision = SQLDate(timestamp)
            
            cursor.execute(CREATE, (
                factura.codigoFactura,
                factura.paciente,
                factura.administrador,
                fecha_emision,
                factura.importeTotal,
                factura.estadoPago
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.create: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_estado(codigoFactura, estadoPago):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                UPDATE_ESTADO,
                (estadoPago, codigoFactura)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.update_estado: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_importe(codigoFactura, importeTotal):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                UPDATE_IMPORTE,
                (importeTotal, codigoFactura)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.update_importe: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete(codigoFactura):
        db = Conexion()
        conn = db.get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute(
                DELETE,
                (codigoFactura,)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error en FacturaDAO.delete: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()