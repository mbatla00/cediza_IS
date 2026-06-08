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
    FamiliarService,
    SesionService
)
from datetime import date, datetime


class PacienteController:
    """Controlador para operaciones de paciente"""

    def __init__(self, nombre_usuario: str):
        self._nombre_usuario = nombre_usuario
        self._paciente_service = PacienteService()
        self._cuestionario_service = CuestionarioService()
        self._respuesta_service = RespuestaService()
        self._familiar_service = FamiliarService()
        self._sesion_service = SesionService()

    # ============================================================
    # PERFIL
    # ============================================================

    def obtener_perfil(self):
        """Retorna el perfil del paciente"""
        return self._paciente_service.obtener_por_nombre(self._nombre_usuario)

    def obtener_perfil_dict(self) -> dict | None:
        """Devuelve un diccionario limpio con los atributos del modelo mapeados"""
        paciente = self._paciente_service.obtener_por_nombre(self._nombre_usuario)
        if not paciente:
            return None
        return {
            "nombre": getattr(paciente, 'nombre', ''),
            "nombreUsuario": getattr(paciente, 'nombreUsuario', ''),
            "dni": getattr(paciente, 'dni', ''),
            "email": getattr(paciente, 'email', ''),
            "telefono": getattr(paciente, 'telefono', ''),
            "fechaNacimiento": getattr(paciente, 'fechaNacimiento', ''),
            "esPublico": getattr(paciente, 'esPublico', ''),
            "numCuenta": getattr(paciente, 'numCuenta', '')
        }

    def actualizar_perfil(self, email: str) -> tuple[bool, str]:
        """Actualiza el email del paciente"""
        return self._paciente_service.actualizar_email(self._nombre_usuario, email)

    def obtener_familiares(self):
        """Retorna los familiares del paciente como VOs"""
        return self._familiar_service.listar_por_paciente(self._nombre_usuario)

    def listar_familiares_dict(self) -> list:
        """Retorna los familiares del paciente como lista de dicts para la vista"""
        familiares = self._familiar_service.listar_por_paciente(self._nombre_usuario)
        return [
            {
                "nombre": getattr(f, 'nombre', ''),
                "relacion": getattr(f, 'Relacion', getattr(f, 'relacion', '')),
                "telefono": getattr(f, 'Telefono', getattr(f, 'telefono', ''))
            }
            for f in (familiares or [])
        ]

    # ============================================================
    # CUESTIONARIOS Y RESPUESTAS
    # ============================================================

    def ya_respondio_hoy(self) -> bool:
        respuestas_hoy = self._respuesta_service.obtener_por_paciente(self._nombre_usuario)
        hoy = date.today()

        for r in respuestas_hoy:
            fecha = self._parsear_fecha(r.fechaHora)
            if fecha == hoy:
                return True

        return False

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
        """Obtiene el historial agrupado por fecha, con respuestas como dicts"""
        respuestas = self._respuesta_service.obtener_por_paciente(self._nombre_usuario)

        historial = {}
        for respuesta in respuestas:
            if not respuesta.fechaHora:
                continue
            fecha_obj = self._parsear_fecha(respuesta.fechaHora)
            if not fecha_obj:
                continue
            if fecha_obj not in historial:
                historial[fecha_obj] = []
            historial[fecha_obj].append({
                "idPregunta": getattr(respuesta, 'idPregunta', None),
                "contenido": getattr(respuesta, 'contenido', '')
            })

        return historial

    def obtener_preguntas_dict(self) -> dict:
        cuestionario = self._cuestionario_service.obtener_diario()
        if not cuestionario:
            return {}
        preguntas = self._cuestionario_service.obtener_preguntas(cuestionario.idCuestionario)
        return {p.idPregunta: p.enunciado for p in preguntas}

    # ============================================================
    # SESIONES
    # ============================================================

    def listar_sesiones(self):
        """Retorna las sesiones del paciente como VOs"""
        return self._sesion_service.obtener_por_paciente(self._nombre_usuario)

    def listar_sesiones_dict(self) -> list:
        """Retorna las sesiones del paciente como lista de dicts para la vista"""
        sesiones = self._sesion_service.obtener_por_paciente(self._nombre_usuario)
        return [
            {
                "fecha": str(getattr(s, 'fecha', '')) if getattr(s, 'fecha', None) else '',
                "hora": str(getattr(s, 'hora', '')) if getattr(s, 'hora', None) else '',
                "especialista": getattr(s, 'especialista', ''),
                "comentarios": getattr(s, 'comentarios', '')
            }
            for s in (sesiones or [])
        ]

    # ============================================================
    # PRIVADO
    # ============================================================

    def _parsear_fecha(self, fecha) -> date | None:
        """Convierte una fecha (str o datetime) a objeto date de forma segura"""
        if not fecha:
            return None
        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha[:10], "%Y-%m-%d").date()
            except ValueError:
                return None
        if hasattr(fecha, 'date'):
            return fecha.date()
        return fecha