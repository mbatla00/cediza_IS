"""
SERVICIO DE COMENTARIOS
"""
from src.modelo.dao import ComentarioDAO


class ComentarioService:
    
    @staticmethod
    def crear(comentario) -> tuple[bool, str]:
        if ComentarioDAO.create(comentario):
            return True, "Comentario guardado correctamente"
        return False, "Error al guardar comentario"
    
    @staticmethod
    def obtener_por_paciente(paciente: str) -> list:
        return ComentarioDAO.get_by_paciente(paciente)