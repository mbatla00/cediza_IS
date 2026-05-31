"""
CONTROLADOR DE TRABAJADOR

Responsabilidad:
- Gestionar operaciones que puede hacer un trabajador
- Ver lista de pacientes
- Añadir comentarios clínicos
- Realizar evaluaciones rápidas
- Gestionar sesiones (si es especialista)
"""
from src.modelo.servicios import (
    PacienteService,
    ComentarioService,
    EvaluacionService,
    SesionService,
    TrabajadorService
)
from src.modelo.vo import Comentario, EvaluacionProfesional
from datetime import date


class TrabajadorController:
    """Controlador para operaciones de trabajador"""
    
    def __init__(self, nombre_usuario: str):
        self._nombre_usuario = nombre_usuario
        self._paciente_service = PacienteService()
        self._comentario_service = ComentarioService()
        self._evaluacion_service = EvaluacionService()
        self._sesion_service = SesionService()
        self._trabajador_service = TrabajadorService()
    
    # ============================================================
    # DATOS DEL PROPIO TRABAJADOR
    # ============================================================
    
    def obtener_tipo_trabajador(self) -> str | None:
        """Retorna el tipo de trabajador"""
        trabajador = self._trabajador_service.obtener_por_nombre(self._nombre_usuario)
        return trabajador.tipo if trabajador else None
    
    def es_especialista(self) -> bool:
        """Verifica si es especialista"""
        return self.obtener_tipo_trabajador() == 'especialista'
    
    # ============================================================
    # PACIENTES
    # ============================================================
    
    def listar_pacientes(self):
        """Retorna todos los pacientes"""
        return self._paciente_service.listar_todos()
    
    def obtener_paciente(self, nombre_usuario: str):
        """Obtiene un paciente específico"""
        return self._paciente_service.obtener_por_nombre(nombre_usuario)
    
    def actualizar_paciente(self, nombre_usuario: str, datos: dict) -> tuple[bool, str]:
        """Actualiza datos de un paciente"""
        paciente = self._paciente_service.obtener_por_nombre(nombre_usuario)
        if not paciente:
            return False, "Paciente no encontrado"
        return self._paciente_service.actualizar(paciente, datos)
    
    # ============================================================
    # COMENTARIOS
    # ============================================================
    
    def agregar_comentario(self, paciente: str, nota: str) -> tuple[bool, str]:
        """Agrega un comentario clínico"""
        if not nota or len(nota.strip()) < 5:
            return False, "La anotación debe tener al menos 5 caracteres"
        
        comentario = Comentario(
            Auxiliar=self._nombre_usuario,
            Paciente=paciente,
            dia=date.today(),
            nota=nota.strip()
        )
        return self._comentario_service.crear(comentario)
    
    def listar_comentarios_de_paciente(self, paciente: str):
        """Retorna todos los comentarios de un paciente"""
        return self._comentario_service.obtener_por_paciente(paciente)
    
    # ============================================================
    # EVALUACIONES
    # ============================================================
    
    def paciente_ya_evaluado_hoy(self, paciente: str) -> bool:
        """Verifica si un paciente ya fue evaluado hoy"""
        evaluaciones = self._evaluacion_service.obtener_por_paciente(paciente)
        hoy = date.today()
        for e in evaluaciones:
            if hasattr(e, 'fecha') and e.fecha == hoy:
                return True
        return False
    
    def guardar_evaluacion(self, datos: dict) -> tuple[bool, str]:
        """Guarda una evaluación rápida"""
        if self.paciente_ya_evaluado_hoy(datos.get('paciente')):
            return False, "Este paciente ya ha sido evaluado hoy"
        
        evaluacion = EvaluacionProfesional(
            Paciente=datos.get('paciente'),
            Trabajador=self._nombre_usuario,
            fecha=date.today(),
            movilidad=datos.get('movilidad'),
            estadoEmocional=datos.get('estadoEmocional'),
            apetito=datos.get('apetito'),
            observaciones=datos.get('observaciones', '')
        )
        return self._evaluacion_service.crear(evaluacion)
    
    def listar_evaluaciones_de_paciente(self, paciente: str):
        """Retorna todas las evaluaciones de un paciente"""
        return self._evaluacion_service.obtener_por_paciente(paciente)
    
    # ============================================================
    # SESIONES (para especialistas)
    # ============================================================
    
    def listar_sesiones_como_especialista(self):
        """Retorna todas las sesiones del especialista actual"""
        if not self.es_especialista():
            return []
        return self._sesion_service.obtener_por_especialista(self._nombre_usuario)
    
    def listar_sesiones_de_paciente(self, paciente: str):
        """Retorna todas las sesiones de un paciente"""
        return self._sesion_service.obtener_por_paciente(paciente)
    
    def crear_sesion(self, datos: dict) -> tuple[bool, str]:
        """Crea una nueva sesión"""
        if not self.es_especialista():
            return False, "Solo los especialistas pueden crear sesiones"
        
        return self._sesion_service.crear({
            **datos,
            'especialista': self._nombre_usuario
        })
    
    def actualizar_sesion(self, id_sesion: int, datos: dict) -> tuple[bool, str]:
        """Actualiza una sesión existente"""
        if not self.es_especialista():
            return False, "Solo los especialistas pueden modificar sesiones"
        
        return self._sesion_service.actualizar(id_sesion, datos, self._nombre_usuario)
    
    def eliminar_sesion(self, id_sesion: int) -> tuple[bool, str]:
        """Elimina una sesión"""
        if not self.es_especialista():
            return False, "Solo los especialistas pueden eliminar sesiones"
        
        return self._sesion_service.eliminar(id_sesion, self._nombre_usuario)