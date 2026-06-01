"""
SERVICIO DE FAMILIARES
"""
from src.modelo.dao import FamiliarDAO
from src.modelo.vo import Familiar
from .usuario_service import UsuarioService


class FamiliarService:
    
    @staticmethod
    def listar_por_paciente(paciente: str) -> list:
        return FamiliarDAO.get_by_paciente(paciente)
    
    @staticmethod
    def crear(datos: dict) -> tuple[bool, str, any]:
        if not datos.get('nombre') or not datos.get('telefono'):
            return False, "Nombre y teléfono son obligatorios", None
        
        if not UsuarioService.validar_telefono(datos['telefono']):
            return False, "Teléfono no válido (9 dígitos)", None
        
        familiar = Familiar(
            Nombre=datos['nombre'],
            Paciente=datos['paciente'],
            Relacion=datos.get('relacion', 'hij@'),
            Telefono=datos['telefono']
        )
        
        if FamiliarDAO.create(familiar):
            return True, "Familiar agregado correctamente", familiar
        return False, "Error al agregar familiar", None
    
    @staticmethod
    def eliminar(nombre: str, paciente: str) -> bool:
        return FamiliarDAO.delete(nombre, paciente)