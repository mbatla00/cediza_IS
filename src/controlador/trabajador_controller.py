"""
CONTROLADOR DE TRABAJADOR

Responsabilidad:
- Gestionar operaciones que puede hacer un trabajador
- Ver lista de pacientes
- Añadir comentarios clínicos
- Realizar evaluaciones rápidas
- Gestionar sesiones (si es especialista)
"""
from src.modelo.logica import (
    PacienteService,
    ComentarioService,
    EvaluacionService,
    SesionService,
    TrabajadorService,
    FamiliarService
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
        self._familiar_service = FamiliarService()
    
    # ============================================================
    # DATOS DEL PROPIO TRABAJADOR
    # ============================================================
    
    def obtener_tipo_trabajador(self) -> str | None:
        trabajador = self._trabajador_service.obtener_por_nombre(self._nombre_usuario)
        return trabajador.tipo if trabajador else None
    
    def es_especialista(self) -> bool:
        tipo = self.obtener_tipo_trabajador()
        return tipo.lower().strip() == 'especialista' if tipo else False

    def obtener_trabajador_dict(self) -> dict | None:
        trabajador = self._trabajador_service.obtener_por_nombre(self._nombre_usuario)
        if not trabajador:
            return None
        return {
            "nombre": getattr(trabajador, 'nombre', ''),
            "nombreUsuario": getattr(trabajador, 'nombreUsuario', ''),
            "dni": getattr(trabajador, 'dni', ''),
            "email": getattr(trabajador, 'email', ''),
            "telefono": getattr(trabajador, 'telefono', ''),
            "fechaNacimiento": getattr(trabajador, 'fechaNacimiento', None)
        }

    def actualizar_trabajador(self, datos: dict) -> tuple[bool, str]:
        trabajador = self._trabajador_service.obtener_por_nombre(self._nombre_usuario)
        if not trabajador:
            return False, "Trabajador no encontrado"
        return self._trabajador_service.actualizar(trabajador, datos)

    # ============================================================
    # PACIENTES
    # ============================================================
    
    def listar_pacientes(self):
        return self._paciente_service.listar_todos()

    def listar_pacientes_dict(self) -> list[dict]:
        pacientes = self._paciente_service.listar_todos()
        return [
            {
                "nombreUsuario": getattr(p, 'nombreUsuario', ''),
                "nombre": getattr(p, 'nombre', ''),
                "tipo": getattr(p, 'tipo', ''),
                "dni": getattr(p, 'dni', '')
            }
            for p in (pacientes or [])
        ]

    def obtener_paciente_dict(self, nombre_usuario: str) -> dict | None:
        p = self._paciente_service.obtener_por_nombre(nombre_usuario)
        if not p:
            return None
        return {
            "nombre": getattr(p, 'nombre', ''),
            "dni": getattr(p, 'dni', ''),
            "telefono": getattr(p, 'telefono', '') or '',
            "tipo": getattr(p, 'tipo', '') or '',
            "diagnostico": getattr(p, 'diagnostico', '') or ''
        }

    def obtener_paciente(self, nombre_usuario: str):
        return self._paciente_service.obtener_por_nombre(nombre_usuario)

    def actualizar_paciente(self, nombre_usuario: str, datos: dict) -> tuple[bool, str]:
        paciente = self._paciente_service.obtener_por_nombre(nombre_usuario)
        if not paciente:
            return False, "Paciente no encontrado"
        return self._paciente_service.actualizar(paciente, datos)

    # ============================================================
    # COMENTARIOS
    # ============================================================
    
    def agregar_comentario(self, paciente: str, nota: str) -> tuple[bool, str]:
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
        return self._comentario_service.obtener_por_paciente(paciente)

    def listar_comentarios_dict(self, paciente: str) -> list[dict]:
        comentarios = self._comentario_service.obtener_por_paciente(paciente)
        return [
            {
                "dia": getattr(c, 'dia', ''),
                "auxiliar": getattr(c, 'auxiliar', getattr(c, 'Auxiliar', '')),
                "nota": getattr(c, 'nota', '')
            }
            for c in (comentarios or [])
        ]

    # ============================================================
    # EVALUACIONES
    # ============================================================
    
    def paciente_ya_evaluado_hoy(self, paciente: str) -> bool:
        evaluaciones = self._evaluacion_service.obtener_por_paciente(paciente)
        hoy = date.today()
        for e in evaluaciones:
            if hasattr(e, 'fecha') and e.fecha == hoy:
                return True
        return False

    def guardar_evaluacion(self, datos: dict) -> tuple[bool, str]:
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
        return self._evaluacion_service.obtener_por_paciente(paciente)

    def listar_evaluaciones_dict(self, paciente: str) -> list[dict]:
        evaluaciones = self._evaluacion_service.obtener_por_paciente(paciente)
        return [
            {
                "fecha": getattr(e, 'fecha', getattr(e, 'dia', '')),
                "dia": getattr(e, 'dia', getattr(e, 'fecha', '')),
                "trabajador": getattr(e, 'trabajador', getattr(e, 'Trabajador', '')),
                "estadoEmocional": getattr(e, 'estadoEmocional', 0),
                "movilidad": getattr(e, 'movilidad', 0),
                "apetito": getattr(e, 'apetito', 0),
                "observaciones": getattr(e, 'observaciones', '')
            }
            for e in (evaluaciones or [])
        ]

    # ============================================================
    # SESIONES
    # ============================================================
    
    def listar_sesiones_como_especialista(self):
        if not self.es_especialista():
            return []
        return self._sesion_service.obtener_por_especialista(self._nombre_usuario)

    def listar_sesiones_dict(self) -> list[dict]:
        if not self.es_especialista():
            return []
        sesiones = self._sesion_service.obtener_por_especialista(self._nombre_usuario)
        return [
            {
                "idSesion": getattr(s, 'idSesion', None),
                "paciente": getattr(s, 'paciente', ''),
                "fecha": str(getattr(s, 'fecha', '')),
                "hora": str(getattr(s, 'hora', '')),
                "comentarios": getattr(s, 'comentarios', '')
            }
            for s in (sesiones or [])
        ]

    def listar_sesiones_de_paciente(self, paciente: str):
        return self._sesion_service.obtener_por_paciente(paciente)

    def listar_sesiones_de_paciente_dict(self, paciente: str) -> list[dict]:
        sesiones = self._sesion_service.obtener_por_paciente(paciente)
        return [
            {
                "fecha": str(getattr(s, 'fecha', '')),
                "hora": str(getattr(s, 'hora', ''))
            }
            for s in (sesiones or [])
        ]

    def crear_sesion(self, datos: dict) -> tuple[bool, str]:
        if not self.es_especialista():
            return False, "Solo los especialistas pueden crear sesiones"
        return self._sesion_service.crear({**datos, 'especialista': self._nombre_usuario})

    def actualizar_sesion(self, id_sesion: int, datos: dict) -> tuple[bool, str]:
        if not self.es_especialista():
            return False, "Solo los especialistas pueden modificar sesiones"
        return self._sesion_service.actualizar(id_sesion, datos, self._nombre_usuario)

    def eliminar_sesion(self, id_sesion: int) -> tuple[bool, str]:
        if not self.es_especialista():
            return False, "Solo los especialistas pueden eliminar sesiones"
        return self._sesion_service.eliminar(id_sesion, self._nombre_usuario)

    # ============================================================
    # FAMILIARES
    # ============================================================

    def listar_familiares_de_paciente(self, paciente: str):
        return self._familiar_service.listar_por_paciente(paciente)

    def listar_familiares_dict(self, paciente: str) -> list[dict]:
        familiares = self._familiar_service.listar_por_paciente(paciente)
        return [
            {
                "nombre": getattr(f, 'nombre', ''),
                "relacion": getattr(f, 'relacion', getattr(f, 'parentesco', '')),
                "telefono": getattr(f, 'telefono', '')
            }
            for f in (familiares or [])
        ]

    def agregar_familiar(self, nombre_paciente: str, nombre: str, parentesco: str, telefono: str) -> tuple[bool, str]:
        return self._familiar_service.crear({
            'paciente': nombre_paciente,
            'nombre': nombre,
            'relacion': parentesco,
            'telefono': telefono
        })