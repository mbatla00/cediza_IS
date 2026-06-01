"""
SERVICIO DE RESPUESTAS
"""
from src.modelo.dao import RespuestaDAO
from src.modelo.vo import Respuesta
from datetime import datetime


class RespuestaService:
    
    @staticmethod
    def obtener_por_paciente(paciente: str) -> list:
        return RespuestaDAO.get_by_paciente(paciente)
    
    @staticmethod
    def guardar_respuestas(paciente: str, respuestas: list[dict]) -> tuple[bool, str]:
        errores = False
        ahora = datetime.now()
        
        for r in respuestas:
            nueva = Respuesta(
                idPregunta=r.get('idPregunta'),
                idPaciente=paciente,
                fechaHora=ahora,
                contenido=r.get('contenido', '')
            )
            if not RespuestaDAO.create(nueva):
                errores = True
        
        if errores:
            return False, "Hubo errores al guardar algunas respuestas"
        return True, "Cuestionario enviado con éxito"