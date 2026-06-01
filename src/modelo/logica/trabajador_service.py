"""
SERVICIO DE TRABAJADORES
"""
from src.modelo.dao import UsuarioDAO, TrabajadorDAO, AuxiliarDAO, CoordinadorDAO, EspecialistaDAO
from src.modelo.vo import Trabajador, Auxiliar, Coordinador, Especialista
from .usuario_service import UsuarioService


class TrabajadorService:
    """Servicio para operaciones CRUD de trabajadores"""
    
    @staticmethod
    def listar_todos() -> list:
        return TrabajadorDAO.get_all()
    
    @staticmethod
    def obtener_por_nombre(nombre_usuario: str):
        return TrabajadorDAO.get_by_nombreUsuario(nombre_usuario)
    
    @staticmethod
    def crear(datos: dict) -> tuple[bool, str, Trabajador | None]:
        if not datos.get('nombre_completo') or not datos.get('nombre_usuario') or not datos.get('dni'):
            return False, "Nombre completo, usuario y DNI son obligatorios", None
        
        if not UsuarioService.validar_dni(datos['dni']):
            return False, "DNI no válido", None
        
        if UsuarioDAO.get_by_nombreUsuario(datos['nombre_usuario']):
            return False, f"El nombre de usuario {datos['nombre_usuario']} ya existe", None
        
        if UsuarioDAO.get_by_dni(datos['dni']):
            return False, f"Ya existe un usuario con DNI {datos['dni']}", None
        
        try:
            nuevo_usuario = Trabajador(
                nombreUsuario=datos['nombre_usuario'],
                Nombre=datos['nombre_completo'],
                DNI=datos['dni'],
                Rol='trabajador',
                password=datos.get('password', datos['dni']),
                Tipo=datos.get('tipo')
            )
            
            if not UsuarioDAO.create(nuevo_usuario):
                return False, "Error al crear la cuenta de usuario", None
            
            if not TrabajadorDAO.create(nuevo_usuario):
                return False, "Error al registrar el trabajador", None
            
            tipo = datos.get('tipo')
            
            if tipo == 'auxiliar':
                auxiliar = Auxiliar(
                    nombreUsuario=datos['nombre_usuario'],
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    Horario=datos.get('horario', 'Mañana')
                )
                if not AuxiliarDAO.create(auxiliar):
                    return False, "Error al registrar el auxiliar", None
                    
            elif tipo == 'coordinador':
                coordinador = Coordinador(
                    nombreUsuario=datos['nombre_usuario'],
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    infoInteres=datos.get('info_interes')
                )
                if not CoordinadorDAO.create(coordinador):
                    return False, "Error al registrar el coordinador", None
                    
            elif tipo == 'especialista':
                especialista = Especialista(
                    nombreUsuario=datos['nombre_usuario'],
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    Especialidad=datos.get('especialidad', ''),
                    Horario=datos.get('horario', '')
                )
                if not EspecialistaDAO.create(especialista):
                    return False, "Error al registrar el especialista", None
            
            return True, f"Trabajador {datos['nombre_completo']} creado correctamente", nuevo_usuario
            
        except Exception as e:
            return False, f"Error crítico: {str(e)}", None