"""
SERVICIO DE EVALUACIONES
"""
from src.modelo.dao import EvaluacionProfesionalDAO


class EvaluacionService:
    
    @staticmethod
    def crear(evaluacion) -> tuple[bool, str]:
        if EvaluacionProfesionalDAO.create(evaluacion):
            return True, "Evaluación guardada correctamente"
        return False, "Error al guardar evaluación"
    
    @staticmethod
    def obtener_por_paciente(paciente: str) -> list:
        return EvaluacionProfesionalDAO.get_by_paciente(paciente)