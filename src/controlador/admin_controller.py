"""
CONTROLADOR DE ADMINISTRADOR
"""
from src.modelo.logica import (
    UsuarioService,
    PacienteService,
    TrabajadorService,
    EnfermedadService,
    FamiliarService
)
from src.modelo.vo import Usuario, Paciente, Trabajador, Familiar


class AdminController:

    def __init__(self):
        self._usuario_service = UsuarioService()
        self._paciente_service = PacienteService()
        self._trabajador_service = TrabajadorService()
        self._enfermedad_service = EnfermedadService()
        self._familiar_service = FamiliarService()

    # ============================================================
    # OPERACIONES CON USUARIOS
    # ============================================================

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuario_service.listar_activos()

    def listar_todos_usuarios(self) -> list[Usuario]:
        return self._usuario_service.listar_todos()

    def listar_todos_usuarios_dict(self) -> list[dict]:
        usuarios = self._usuario_service.listar_todos()
        resultado = []
        for u in (usuarios or []):
            rol = getattr(u, 'rol', '').lower()
            tipo = getattr(u, 'tipo', '').lower() or rol
            nombre_usuario = getattr(u, 'nombreUsuario', '')

            if rol == 'trabajador':
                trabajador = self._trabajador_service.obtener_por_nombre(nombre_usuario)
                tipo = getattr(trabajador, 'tipo', 'trabajador').lower() if trabajador else 'trabajador'

            elif rol == 'paciente':
                paciente = self._paciente_service.obtener_por_nombre(nombre_usuario)
                tipo = getattr(paciente, 'tipo', 'paciente').lower() if paciente else 'paciente'

            resultado.append({
                "nombre": getattr(u, 'nombre', 'Sin nombre'),
                "nombreUsuario": nombre_usuario,
                "tipo": tipo
            })
        return resultado
    
    def listar_usuarios_activos_dict(self) -> list[dict]:
        """Devuelve únicamente los usuarios activos en formato diccionario para la vista."""
        usuarios = self._usuario_service.listar_activos()
        resultado = []
        for u in (usuarios or []):
            rol = getattr(u, 'rol', '').lower()
            tipo = getattr(u, 'tipo', '').lower() or rol
            nombre_usuario = getattr(u, 'nombreUsuario', '')

            if rol == 'trabajador':
                trabajador = self._trabajador_service.obtener_por_nombre(nombre_usuario)
                tipo = getattr(trabajador, 'tipo', 'trabajador').lower() if trabajador else 'trabajador'
            elif rol == 'paciente':
                paciente = self._paciente_service.obtener_por_nombre(nombre_usuario)
                tipo = getattr(paciente, 'tipo', tipo) if paciente else tipo

            resultado.append({
                'nombre': getattr(u, 'nombre', ''),
                'nombreUsuario': nombre_usuario,
                'tipo': tipo
            })
        return resultado

    def obtener_usuario(self, nombre_usuario: str) -> Usuario | None:
        return self._usuario_service.obtener_por_nombre(nombre_usuario)

    def actualizar_usuario(self, nombre_usuario: str, nuevos_datos: dict) -> tuple[bool, str]:
        usuario = self._usuario_service.obtener_por_nombre(nombre_usuario)
        if not usuario:
            return False, "Usuario no encontrado"
        return self._usuario_service.actualizar(usuario, nuevos_datos)

    def cambiar_estado_usuario(self, nombre_usuario: str, desactivar: bool) -> tuple[bool, str]:
        if desactivar:
            return self._usuario_service.desactivar(nombre_usuario)
        else:
            return self._usuario_service.activar(nombre_usuario)

    def crear_administrador(self, datos: dict) -> tuple[bool, str]:
        return self._usuario_service.crear_administrador(datos)

    # ============================================================
    # OPERACIONES CON PACIENTES
    # ============================================================

    def crear_paciente(self, datos: dict) -> tuple[bool, str, Paciente | None]:
        return self._paciente_service.crear(datos)

    def listar_pacientes(self) -> list[Paciente]:
        return self._paciente_service.listar_todos()

    def obtener_paciente(self, nombre_usuario: str) -> Paciente | None:
        return self._paciente_service.obtener_por_nombre(nombre_usuario)

    def actualizar_paciente(self, paciente: Paciente, datos: dict) -> tuple[bool, str]:
        return self._paciente_service.actualizar(paciente, datos)

    # ============================================================
    # OPERACIONES CON TRABAJADORES
    # ============================================================

    def crear_trabajador(self, datos: dict) -> tuple[bool, str, Trabajador | None]:
        return self._trabajador_service.crear(datos)

    def listar_trabajadores(self) -> list[Trabajador]:
        return self._trabajador_service.listar_todos()

    def obtener_trabajador(self, nombre_usuario: str) -> Trabajador | None:
        return self._trabajador_service.obtener_por_nombre(nombre_usuario)

    # ============================================================
    # OPERACIONES CON ENFERMEDADES
    # ============================================================

    def listar_enfermedades(self) -> list[dict]:
        return self._enfermedad_service.listar_todas()

    def agregar_enfermedad(self, nombre: str) -> tuple[bool, str, int | None]:
        return self._enfermedad_service.crear(nombre)

    def asignar_enfermedad_a_paciente(self, paciente: str, enfermedad_id: int) -> bool:
        return self._enfermedad_service.asignar_a_paciente(paciente, enfermedad_id)

    def eliminar_enfermedad_de_paciente(self, paciente: str, enfermedad_id: int) -> bool:
        return self._enfermedad_service.eliminar_de_paciente(paciente, enfermedad_id)

    # ============================================================
    # OPERACIONES CON FAMILIARES
    # ============================================================

    def listar_familiares_de_paciente(self, paciente: str) -> list[Familiar]:
        return self._familiar_service.listar_por_paciente(paciente)

    def agregar_familiar(self, datos: dict) -> tuple[bool, str, Familiar | None]:
        return self._familiar_service.crear(datos)

    def eliminar_familiar(self, nombre: str, paciente: str) -> bool:
        return self._familiar_service.eliminar(nombre, paciente)

    # ============================================================
    # MÉTODOS PUENTE PARA LAS VISTAS
    # ============================================================

    def agregar_paciente(self, datos: dict) -> tuple[bool, str, str | None]:
        tipo_raw = datos.get('tipoPaciente', '').lower()
        tipo = 'publico' if 'pub' in tipo_raw else 'privado'

        datos_servicio = {
            'nombre_completo': datos.get('nombre'),
            'nombre_usuario': datos.get('nombreUsuario') or None,
            'dni': datos.get('dni'),
            'fecha_nacimiento': datos.get('fechaNacimiento'),
            'telefono': datos.get('telefono'),
            'email': datos.get('email'),
            'password': datos.get('password') or datos.get('dni'),
            'tipo': tipo,
            'cuenta': datos.get('cuentaBancaria')
        }

        exito, msg, paciente = self._paciente_service.crear(datos_servicio)
        return exito, msg, paciente.nombreUsuario if paciente else None

    def agregar_trabajador(self, datos: dict) -> tuple[bool, str, object | None]:
        tipo_baja = datos.get('tipo', '').lower()
        datos_servicio = {
            'nombre_completo': datos.get('nombre'),
            'nombre_usuario': datos.get('usuario'),
            'dni': datos.get('dni'),
            'telefono': datos.get('telefono') or None,
            'email': datos.get('email') or None,
            'password': datos.get('password') or datos.get('dni'),
            'tipo': tipo_baja,
            'especialidad': datos.get('especialidad', '') if tipo_baja == 'especialista' else '',
            'horario': 'Mañana/Tarde',
            'info_interes': ''
        }
        return self._trabajador_service.crear(datos_servicio)

    def agregar_administrador(self, datos: dict) -> tuple[bool, str, None]:
        exito, msg = self._usuario_service.crear_administrador(datos)
        return exito, msg, None

    def obtener_usuario_dict(self, nombre_usuario: str) -> dict | None:
        usuario = self._usuario_service.obtener_por_nombre(nombre_usuario)
        if not usuario:
            return None

        rol = getattr(usuario, 'rol', '').lower()
        tipo = getattr(usuario, 'tipo', '').lower() or rol

        if rol == 'trabajador':
            trabajador = self._trabajador_service.obtener_por_nombre(nombre_usuario)
            tipo = getattr(trabajador, 'tipo', 'trabajador').lower() if trabajador else 'trabajador'

        datos = {
            "nombre": getattr(usuario, 'nombre', ''),
            "nombreUsuario": getattr(usuario, 'nombreUsuario', ''),
            "dni": getattr(usuario, 'dni', ''),
            "email": getattr(usuario, 'email', ''),
            "telefono": getattr(usuario, 'telefono', ''),
            "fechaNacimiento": getattr(usuario, 'fechaNacimiento', None),
            "tipo": tipo
        }

        if tipo in ('auxiliar', 'especialista', 'coordinador'):
            trabajador = self._trabajador_service.obtener_por_nombre(nombre_usuario)
            datos["especialidad"] = getattr(trabajador, 'especialidad', '') if trabajador else ''
            datos["horario"] = getattr(trabajador, 'horario', '') if trabajador else ''

        elif tipo in ('paciente', 'publico', 'privado'):
            paciente = self._paciente_service.obtener_por_nombre(nombre_usuario)
            datos["tipo"] = getattr(paciente, 'tipo', tipo) if paciente else tipo
            datos["enfermedades"] = []
            datos["contactos"] = []

        return datos
    

    def cambiar_estado_usuario(self, nombre_usuario: str, activar: bool) -> tuple[bool, str]:
        """Llama al servicio para cambiar el estado lógico del usuario."""
        return self._usuario_service.cambiar_estado(nombre_usuario, activar)

    def esta_activo(self, nombre_usuario: str) -> bool:
        """Devuelve True si el usuario está activo, False si está desactivado."""
        usuario = self._usuario_service.obtener_por_nombre(nombre_usuario)
        if usuario:
            return getattr(usuario, 'activo', True) 
        return False