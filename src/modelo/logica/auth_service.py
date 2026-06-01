"""
SERVICIO DE AUTENTICACIÓN
"""
from src.modelo.dao import UsuarioDAO


class AuthService:
    """Servicio para autenticación de usuarios"""
    
    @staticmethod
    def autenticar(nombre_usuario: str, password: str) -> tuple[bool, str, any]:
        """Autentica un usuario"""
        if not nombre_usuario or not password:
            return False, "Usuario y contraseña son obligatorios", None
        
        usuario = UsuarioDAO.get_by_nombreUsuario(nombre_usuario)
        
        if not usuario:
            return False, "Usuario no encontrado", None
        
        if usuario.password != password:
            return False, "Contraseña incorrecta", None
        
        if hasattr(usuario, 'activo') and not usuario.activo:
            return False, "Usuario desactivado. Contacte con administrador", None
        
        return True, "Autenticación exitosa", usuario