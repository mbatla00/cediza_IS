"""
SERVICIO DE USUARIOS

Contiene la lógica de negocio para operaciones con usuarios.
Usa UsuarioDAO para acceder a la base de datos.
"""
from src.modelo.dao import UsuarioDAO
from src.modelo.conexion.Conexion import Conexion
import re


class UsuarioService:
    """Servicio para operaciones CRUD de usuarios"""
    
    @staticmethod
    def listar_activos() -> list:
        """Retorna todos los usuarios activos"""
        todos = UsuarioDAO.get_all()
        return [u for u in todos if getattr(u, 'activo', True)]
    
    @staticmethod
    def listar_todos() -> list:
        """Retorna todos los usuarios (incluyendo inactivos)"""
        return UsuarioDAO.get_all()
    
    @staticmethod
    def obtener_por_nombre(nombre_usuario: str):
        """Retorna un usuario por su nombre de usuario"""
        return UsuarioDAO.get_by_nombreUsuario(nombre_usuario)
    
    @staticmethod
    def obtener_por_dni(dni: str):
        """Retorna un usuario por su DNI"""
        return UsuarioDAO.get_by_dni(dni)
    
    @staticmethod
    def validar_dni(dni: str) -> bool:
        """Valida un DNI español"""
        if not re.match(r'^\d{8}[A-Za-z]$', dni):
            return False
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:-1])
        letra = dni[-1].upper()
        return letras[numero % 23] == letra
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida un teléfono español de 9 dígitos"""
        if not telefono:
            return True
        return bool(re.match(r'^\d{9}$', telefono))
    
    @staticmethod
    def actualizar(usuario, nuevos_datos: dict) -> tuple[bool, str]:
        """Actualiza los datos de un usuario"""
        try:
            if 'nombre' in nuevos_datos:
                usuario._nombre = nuevos_datos['nombre']
            if 'email' in nuevos_datos:
                usuario._email = nuevos_datos['email']
            if 'dni' in nuevos_datos:
                if not UsuarioService.validar_dni(nuevos_datos['dni']):
                    return False, "DNI no válido"
                usuario._dni = nuevos_datos['dni']
            if 'password' in nuevos_datos and nuevos_datos['password']:
                usuario._password = nuevos_datos['password']
            
            exito = UsuarioDAO.update(usuario)
            if exito:
                return True, "Usuario actualizado correctamente"
            return False, "Error al actualizar en la base de datos"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def desactivar(nombre_usuario: str) -> tuple[bool, str]:
        """Desactiva un usuario (baja lógica)"""
        try:
            exito = UsuarioDAO.delete(nombre_usuario)
            if exito:
                return True, f"Usuario {nombre_usuario} desactivado correctamente"
            return False, "Error al desactivar usuario"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def activar(nombre_usuario: str) -> tuple[bool, str]:
        """Re-activa un usuario"""
        db = Conexion()
        conn = db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Usuarios SET activo = 1 WHERE nombreUsuario = ?",
                (nombre_usuario,)
            )
            conn.commit()
            return True, f"Usuario {nombre_usuario} reactivado correctamente"
        except Exception as e:
            conn.rollback()
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()
    
    @staticmethod
    def crear_administrador(datos: dict) -> tuple[bool, str]:
        """Crea un nuevo administrador"""
        from src.modelo.vo import Admin
        
        if not datos.get('nombre_completo') or not datos.get('nombre_usuario'):
            return False, "Nombre completo y nombre de usuario son obligatorios"
        
        if not UsuarioService.validar_dni(datos.get('dni', '')):
            return False, "DNI no válido"
        
        if datos.get('telefono') and not UsuarioService.validar_telefono(datos['telefono']):
            return False, "Teléfono no válido (deben ser 9 dígitos)"
        
        if UsuarioDAO.get_by_nombreUsuario(datos['nombre_usuario']):
            return False, f"El nombre de usuario {datos['nombre_usuario']} ya existe"
        
        if UsuarioDAO.get_by_dni(datos['dni']):
            return False, f"Ya existe un usuario con DNI {datos['dni']}"
        
        try:
            nuevo_admin = Admin(
                nombreUsuario=datos['nombre_usuario'],
                Nombre=datos['nombre_completo'],
                DNI=datos['dni'],
                password=datos.get('password', datos['dni'])
            )
            
            if not UsuarioDAO.create(nuevo_admin):
                return False, "Error al crear la cuenta de administrador"
            
            if datos.get('telefono'):
                db = Conexion()
                conn = db.get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE Usuarios SET telefono = ? WHERE nombreUsuario = ?",
                            (datos['telefono'], datos['nombre_usuario'])
                        )
                        conn.commit()
                    except Exception:
                        pass
                    finally:
                        cursor.close()
            
            from src.modelo.dao import AdministradorDAO
            
            class TempAdmin:
                def __init__(self, nombreUsuario):
                    self.nombreUsuario = nombreUsuario
            
            admin_reg = TempAdmin(datos['nombre_usuario'])
            if not AdministradorDAO.create(admin_reg):
                return False, "Error al crear registro de administrador"
            
            return True, f"Administrador {datos['nombre_completo']} creado correctamente"
        except Exception as e:
            return False, f"Error crítico: {str(e)}"