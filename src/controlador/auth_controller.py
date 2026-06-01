"""
CONTROLADOR DE AUTENTICACIÓN

Responsabilidad:
- Gestionar el inicio y cierre de sesión de usuarios
- Mantener el usuario actual en sesión
- Verificar permisos según el rol

NO contiene:
- DAOs
- SQL
- Conexiones a BD
- Lógica de negocio compleja

La autenticación real la hace AuthService (en modelo/servicios/)
"""
from src.modelo.logica import AuthService
from src.modelo.vo import Usuario


class AuthController:
    """
    Controlador para autenticación.
    La vista (PySide6) usa este controlador para login/logout.
    """
    
    def __init__(self):
        """Inicializa el controlador con el servicio de autenticación"""
        # El servicio contiene la lógica de negocio (validar contra BD)
        self._auth_service = AuthService()
        
        # Usuario actualmente logueado (None si no hay sesión)
        self._usuario_actual = None
    
    def login(self, nombre_usuario: str, password: str) -> tuple[bool, str, Usuario | None]:
        """
        Intenta iniciar sesión con las credenciales proporcionadas.
        
        Args:
            nombre_usuario: Nombre de usuario ingresado
            password: Contraseña ingresada
        
        Returns:
            tuple[bool, str, Usuario | None]:
                - bool: True si el login fue exitoso, False si no
                - str: Mensaje para mostrar al usuario
                - Usuario | None: El objeto VO del usuario si éxito, None si no
        """
        # Delegamos toda la lógica al servicio
        exito, mensaje, usuario = self._auth_service.autenticar(nombre_usuario, password)
        
        # Si el login es exitoso, guardamos el usuario en la "sesión"
        if exito and usuario:
            self._usuario_actual = usuario
        
        return exito, mensaje, usuario
    
    def logout(self) -> None:
        """Cierra la sesión actual"""
        self._usuario_actual = None
    
    def get_usuario_actual(self) -> Usuario | None:
        """Retorna el usuario actualmente logueado"""
        return self._usuario_actual
    
    def get_rol_actual(self) -> str | None:
        """Retorna el rol del usuario actual"""
        if self._usuario_actual:
            return self._usuario_actual.rol
        return None
    
    def get_nombre_usuario_actual(self) -> str | None:
        """Retorna el nombre de usuario del actual"""
        if self._usuario_actual:
            return self._usuario_actual.nombreUsuario
        return None
    
    def tiene_permiso(self, roles_permitidos: list[str]) -> bool:
        """
        Verifica si el usuario actual tiene alguno de los roles permitidos.
        
        Args:
            roles_permitidos: Lista de roles que pueden acceder
        
        Returns:
            bool: True si tiene permiso
        """
        if not self._usuario_actual:
            return False
        return self._usuario_actual.rol in roles_permitidos
    
    def redirigir_segun_rol(self) -> str:
        """
        Determina qué vista debe mostrar según el rol del usuario.
        
        Returns:
            str: 'admin_dashboard', 'trabajador_dashboard', 'paciente_dashboard' o 'login'
        """
        if not self._usuario_actual:
            return "login"
        
        rol = self._usuario_actual.rol
        mapeo = {
            'admin': 'admin_dashboard',
            'trabajador': 'trabajador_dashboard',
            'paciente': 'paciente_dashboard'
        }
        return mapeo.get(rol, 'login')
    
    def esta_logueado(self) -> bool:
        """Verifica si hay un usuario logueado"""
        return self._usuario_actual is not None