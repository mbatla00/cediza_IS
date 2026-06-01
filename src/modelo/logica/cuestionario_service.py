"""
SERVICIO DE CUESTIONARIOS
"""
from src.modelo.dao import CuestionarioDAO, PreguntaDAO


class CuestionarioService:
    
    @staticmethod
    def obtener_diario():
        cuestionarios = CuestionarioDAO.get_all()
        return next((c for c in cuestionarios if c.tipo == 'diario'), None)
    
    @staticmethod
    def obtener_preguntas(id_cuestionario: int):
        return PreguntaDAO.get_by_cuestionario(id_cuestionario)