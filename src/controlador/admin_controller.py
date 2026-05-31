"""
CONTROLADOR DE ADMINISTRADOR

Responsabilidad:
- Gestionar operaciones que solo puede hacer un administrador
- Crear/editar/eliminar usuarios, pacientes, trabajadores
- Gestionar enfermedades y familiares

NO contiene:
- DAOs, SQL, conexiones a BD
"""
from src.modelo.servicios import (
    UsuarioService,
    PacienteService,
    TrabajadorService,
    EnfermedadService,
    FamiliarService
)
from src.modelo.vo import Usuario, Paciente, Trabajador, Familiar


class AdminController:
    """Controlador para operaciones de administrador"""
    
    def __init__(self):
        """Inicializa todos los servicios necesarios para el administrador"""
        self._usuario_service = UsuarioService()
        self._paciente_service = PacienteService()
        self._trabajador_service = TrabajadorService()
        self._enfermedad_service = EnfermedadService()
        self._familiar_service = FamiliarService()
    
    # ============================================================
    # OPERACIONES CON USUARIOS
    # ============================================================
    
    def listar_usuarios(self) -> list[Usuario]:
        """Retorna lista de todos los usuarios activos"""
        return self._usuario_service.listar_activos()
    
    def listar_todos_usuarios(self) -> list[Usuario]:
        """Retorna lista de TODOS los usuarios (incluyendo inactivos)"""
        return self._usuario_service.listar_todos()
    
    def obtener_usuario(self, nombre_usuario: str) -> Usuario | None:
        """Obtiene un usuario por su nombre"""
        return self._usuario_service.obtener_por_nombre(nombre_usuario)
    
    def actualizar_usuario(self, usuario: Usuario, nuevos_datos: dict) -> tuple[bool, str]:
        """Actualiza los datos de un usuario"""
        return self._usuario_service.actualizar(usuario, nuevos_datos)
    
    def cambiar_estado_usuario(self, nombre_usuario: str, desactivar: bool) -> tuple[bool, str]:
        """Activa o desactiva un usuario"""
        if desactivar:
            return self._usuario_service.desactivar(nombre_usuario)
        else:
            return self._usuario_service.activar(nombre_usuario)
    
    def crear_administrador(self, datos: dict) -> tuple[bool, str]:
        """Crea un nuevo administrador"""
        return self._usuario_service.crear_administrador(datos)
    
    # ============================================================
    # OPERACIONES CON PACIENTES
    # ============================================================
    
    def crear_paciente(self, datos: dict) -> tuple[bool, str, Paciente | None]:
        """Crea un nuevo paciente"""
        return self._paciente_service.crear(datos)
    
    def listar_pacientes(self) -> list[Paciente]:
        """Retorna todos los pacientes activos"""
        return self._paciente_service.listar_todos()
    
    def obtener_paciente(self, nombre_usuario: str) -> Paciente | None:
        """Obtiene un paciente por su nombre"""
        return self._paciente_service.obtener_por_nombre(nombre_usuario)
    
    def actualizar_paciente(self, paciente: Paciente, datos: dict) -> tuple[bool, str]:
        """Actualiza datos de un paciente"""
        return self._paciente_service.actualizar(paciente, datos)
    
    # ============================================================
    # OPERACIONES CON TRABAJADORES
    # ============================================================
    
    def crear_trabajador(self, datos: dict) -> tuple[bool, str, Trabajador | None]:
        """Crea un nuevo trabajador"""
        return self._trabajador_service.crear(datos)
    
    def listar_trabajadores(self) -> list[Trabajador]:
        """Retorna todos los trabajadores"""
        return self._trabajador_service.listar_todos()
    
    def obtener_trabajador(self, nombre_usuario: str) -> Trabajador | None:
        """Obtiene un trabajador por su nombre"""
        return self._trabajador_service.obtener_por_nombre(nombre_usuario)
    
    # ============================================================
    # OPERACIONES CON ENFERMEDADES
    # ============================================================
    
    def listar_enfermedades(self) -> list[dict]:
        """Retorna todas las enfermedades disponibles"""
        return self._enfermedad_service.listar_todas()
    
    def agregar_enfermedad(self, nombre: str) -> tuple[bool, str, int | None]:
        """Agrega una nueva enfermedad"""
        return self._enfermedad_service.crear(nombre)
    
    def asignar_enfermedad_a_paciente(self, paciente: str, enfermedad_id: int) -> bool:
        """Asigna una enfermedad a un paciente"""
        return self._enfermedad_service.asignar_a_paciente(paciente, enfermedad_id)
    
    def eliminar_enfermedad_de_paciente(self, paciente: str, enfermedad_id: int) -> bool:
        """Elimina una enfermedad de un paciente"""
        return self._enfermedad_service.eliminar_de_paciente(paciente, enfermedad_id)
    
    # ============================================================
    # OPERACIONES CON FAMILIARES
    # ============================================================
    
    def listar_familiares_de_paciente(self, paciente: str) -> list[Familiar]:
        """Retorna los familiares de un paciente"""
        return self._familiar_service.listar_por_paciente(paciente)
    
    def agregar_familiar(self, datos: dict) -> tuple[bool, str, Familiar | None]:
        """Agrega un familiar a un paciente"""
        return self._familiar_service.crear(datos)
    
    def eliminar_familiar(self, nombre: str, paciente: str) -> bool:
        """Elimina un familiar de un paciente"""
        return self._familiar_service.eliminar(nombre, paciente)