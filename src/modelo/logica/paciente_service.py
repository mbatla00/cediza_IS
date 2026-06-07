"""
SERVICIO DE PACIENTES
"""
from src.modelo.dao import UsuarioDAO, PacienteDAO, PacPubDAO, PacPriDAO
from src.modelo.vo import Paciente, PacPub, PacPri
from .usuario_service import UsuarioService


class PacienteService:

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

        # Acepta tanto 'fechaNacimiento' como 'fecha_nacimiento'
        fecha = datos.get('fechaNacimiento') or datos.get('fecha_nacimiento')

        try:
            if datos.get('tipo') == 'publico':
                nuevo_pac = PacPub(
                    nombreUsuario=nombre_usuario,
                    Nombre=datos['nombre_completo'],
                    DNI=datos['dni'],
                    password=datos.get('password', datos['dni']),
                    Dias_ingresado=0,
                    email=datos.get('email'),
                    fechaNacimiento=fecha,
                    telefono=datos.get('telefono'),
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
                    email=datos.get('email'),
                    fechaNacimiento=fecha,
                    telefono=datos.get('telefono'),
                )
                exito = (
                    UsuarioDAO.create(nuevo_pac) and
                    PacienteDAO.create(nuevo_pac) and
                    PacPriDAO.create(nuevo_pac)
                )

            if not exito:
                return False, "Error al guardar datos del paciente", None

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
            if 'nombre' in datos:
                paciente._nombre = datos['nombre']
            if 'email' in datos:
                paciente._email = datos['email']
            if 'dni' in datos:
                paciente._dni = datos['dni']
            if 'password' in datos and datos['password']:
                paciente._password = datos['password']

            # Acepta tanto 'fechaNacimiento' como 'fecha_nacimiento'
            fecha = datos.get('fechaNacimiento') or datos.get('fecha_nacimiento')
            if fecha:
                paciente._fechaNacimiento = fecha

            telefono = datos.get('telefono')
            if telefono:
                paciente._telefono = telefono

            exito = UsuarioDAO.update(paciente)

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