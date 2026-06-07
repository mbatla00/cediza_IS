"""
SERVICIO DE PACIENTES
"""
from src.modelo.dao import UsuarioDAO, PacienteDAO, PacPubDAO, PacPriDAO
from src.modelo.vo import Paciente, PacPub, PacPri
from .usuario_service import UsuarioService


class PacienteService:
    """Servicio para operaciones CRUD de pacientes"""

    @staticmethod
    def listar_todos() -> list:
        return PacienteDAO.get_all()

    @staticmethod
    def obtener_por_nombre(nombre_usuario: str):
        return PacienteDAO.get_by_nombreUsuario(nombre_usuario)

    @staticmethod
    def crear(datos: dict) -> tuple[bool, str, Paciente | None]:
        if not datos.get('nombre_completo') or not datos.get('dni'):
            return False, "Nombre completo y DNI son obligatorios", None

        if not UsuarioService.validar_dni(datos['dni']):
            return False, "DNI no válido", None

        if datos.get('telefono') and not UsuarioService.validar_telefono(datos['telefono']):
            return False, "Teléfono no válido (9 dígitos)", None

        nombre_usuario = datos.get('nombre_usuario')
        if not nombre_usuario:
            nombre_usuario = datos['nombre_completo'].replace(' ', '').lower()[:50]

        if UsuarioDAO.get_by_nombreUsuario(nombre_usuario):
            return False, f"El nombre de usuario {nombre_usuario} ya existe", None

        if UsuarioDAO.get_by_dni(datos['dni']):
            return False, f"Ya existe un usuario con DNI {datos['dni']}", None

        try:
            # Se usa directamente PacPub o PacPri (subclases concretas)
            # para evitar instanciar Paciente que es clase abstracta
            if datos.get('tipo') == 'publico':
                nuevo_pac = PacPub(
                    nombreUsuario=nombre_usuario,
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    Dias_ingresado=0,
                    email=datos.get('email')
                )
                exito = (
                    UsuarioDAO.create(nuevo_pac) and
                    PacienteDAO.create(nuevo_pac) and
                    PacPubDAO.create(nuevo_pac)
                )
            else:
                if not datos.get('cuenta'):
                    return False, "Los pacientes privados necesitan cuenta bancaria", None
                nuevo_pac = PacPri(
                    nombreUsuario=nombre_usuario,
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    cuenta=datos['cuenta'],
                    email=datos.get('email')
                )
                exito = (
                    UsuarioDAO.create(nuevo_pac) and
                    PacienteDAO.create(nuevo_pac) and
                    PacPriDAO.create(nuevo_pac)
                )

            if not exito:
                return False, "Error al guardar datos del paciente", None

            if datos.get('telefono'):
                UsuarioDAO.update_telefono(nombre_usuario, datos['telefono'])

            return True, "Paciente creado correctamente", nuevo_pac

        except Exception as e:
            return False, f"Error crítico: {str(e)}", None

    @staticmethod
    def actualizar(paciente: Paciente, datos: dict) -> tuple[bool, str]:
        if datos.get('telefono') and not UsuarioService.validar_telefono(datos['telefono']):
            return False, "Teléfono no válido (9 dígitos)"

        if 'dni' in datos and not UsuarioService.validar_dni(datos['dni']):
            return False, "DNI no válido"

        try:
            # Mutación directa del objeto concreto (PacPub o PacPri)
            # Necesario porque Paciente es clase abstracta y no se puede reinstanciar
            if 'nombre' in datos:
                paciente._nombre = datos['nombre']
            if 'email' in datos:
                paciente._email = datos['email']
            if 'dni' in datos:
                paciente._dni = datos['dni']
            if 'fecha_nacimiento' in datos:
                paciente._fechaNacimiento = datos['fecha_nacimiento']

            exito = UsuarioDAO.update(paciente)

            if datos.get('telefono'):
                UsuarioDAO.update_telefono(paciente.nombreUsuario, datos['telefono'])

            if exito:
                return True, "Paciente actualizado correctamente"
            return False, "Error al actualizar"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def actualizar_email(nombre_usuario: str, email: str) -> tuple[bool, str]:
        paciente = PacienteService.obtener_por_nombre(nombre_usuario)
        if not paciente:
            return False, "Paciente no encontrado"
        return PacienteService.actualizar(paciente, {'email': email})