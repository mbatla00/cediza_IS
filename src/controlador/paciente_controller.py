"""
CONTROLADOR DE PACIENTE

Responsabilidad:
- Gestionar operaciones que puede hacer un paciente
- Ver/editar su perfil
- Responder cuestionarios diarios
- Ver su historial médico
"""
from src.modelo.logica import (
    PacienteService,
    CuestionarioService,
    RespuestaService,
    FamiliarService
)
from datetime import date


class PacienteController:
    """Controlador para operaciones de paciente"""
    
    def __init__(self, nombre_usuario: str):
        self._nombre_usuario = nombre_usuario
        self._paciente_service = PacienteService()
        self._cuestionario_service = CuestionarioService()
        self._respuesta_service = RespuestaService()
        self._familiar_service = FamiliarService()
    
    # ============================================================
    # PERFIL
    # ============================================================
    
    def obtener_perfil(self):
        """Retorna el perfil del paciente"""
        return self._paciente_service.obtener_por_nombre(self._nombre_usuario)
    
    def actualizar_perfil(self, email: str) -> tuple[bool, str]:
        """Actualiza el email del paciente"""
        return self._paciente_service.actualizar_email(self._nombre_usuario, email)
    
    def obtener_familiares(self):
        """Retorna los familiares del paciente"""
        return self._familiar_service.listar_por_paciente(self._nombre_usuario)
    
    # ============================================================
    # CUESTIONARIO DIARIO
    # ============================================================
    
    def ya_respondio_hoy(self) -> bool:
        """Verifica si ya respondió el cuestionario hoy"""
        respuestas_hoy = self._respuesta_service.obtener_por_paciente(self._nombre_usuario)
        hoy = date.today()
        return any(r.fechaHora and r.fechaHora.date() == hoy for r in respuestas_hoy)
    
    def obtener_cuestionario_diario(self):
        """Obtiene el cuestionario diario"""
        return self._cuestionario_service.obtener_diario()
    
    def obtener_preguntas_del_cuestionario(self, id_cuestionario: int):
        """Obtiene las preguntas de un cuestionario"""
        return self._cuestionario_service.obtener_preguntas(id_cuestionario)
    
    def guardar_respuestas(self, respuestas: list[dict]) -> tuple[bool, str]:
        """Guarda múltiples respuestas"""
        return self._respuesta_service.guardar_respuestas(self._nombre_usuario, respuestas)
    
    # ============================================================
    # HISTORIAL
    # ============================================================
    
    def obtener_historial(self):
        """Obtiene el historial de respuestas"""
        return self._respuesta_service.obtener_por_paciente(self._nombre_usuario)
    
    def obtener_historial_agrupado_por_fecha(self) -> dict:
        """Obtiene el historial agrupado por fecha"""
        respuestas = self._respuesta_service.obtener_por_paciente(self._nombre_usuario)
        
        historial = {}
        for respuesta in respuestas:
            if respuesta.fechaHora:
                fecha = respuesta.fechaHora.date()
                if fecha not in historial:
                    historial[fecha] = []
                historial[fecha].append(respuesta)
        
        return historial