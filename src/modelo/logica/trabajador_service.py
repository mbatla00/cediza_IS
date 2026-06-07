"""
SERVICIO DE TRABAJADORES
"""
from src.modelo.dao import UsuarioDAO, TrabajadorDAO, AuxiliarDAO, CoordinadorDAO, EspecialistaDAO
from src.modelo.vo import Trabajador, Auxiliar, Coordinador, Especialista
from .usuario_service import UsuarioService


class TrabajadorService:
    """Servicio para operaciones CRUD de trabajadores"""

    @staticmethod
    def listar_todos() -> list:
        return TrabajadorDAO.get_all()

    @staticmethod
    def obtener_por_nombre(nombre_usuario: str):
        return TrabajadorDAO.get_by_nombreUsuario(nombre_usuario)

    @staticmethod
    def crear(datos: dict) -> tuple[bool, str, Trabajador | None]:
        if not datos.get('nombre_completo') or not datos.get('nombre_usuario') or not datos.get('dni'):
            return False, "Nombre completo, usuario y DNI son obligatorios", None

        if not UsuarioService.validar_dni(datos['dni']):
            return False, "DNI no válido", None

        if UsuarioDAO.get_by_nombreUsuario(datos['nombre_usuario']):
            return False, f"El nombre de usuario {datos['nombre_usuario']} ya existe", None

        if UsuarioDAO.get_by_dni(datos['dni']):
            return False, f"Ya existe un usuario con DNI {datos['dni']}", None

        try:
            tipo = datos.get('tipo_trabajador') or datos.get('tipo')

            common = dict(
                nombreUsuario=datos['nombre_usuario'],
                Nombre=datos['nombre_completo'],
                DNI=datos['dni'],
                password=datos.get('password', datos['dni']),
                email=datos.get('email'),
                fechaNacimiento=datos.get('fecha_nacimiento'),
                telefono=datos.get('telefono'),
            )

            if tipo == 'auxiliar':
                nuevo_usuario = Auxiliar(**common, Horario=datos.get('horario', 'Mañana'))
            elif tipo == 'coordinador':
                nuevo_usuario = Coordinador(**common, infoInteres=datos.get('info_interes'))
            elif tipo == 'especialista':
                nuevo_usuario = Especialista(
                    **common,
                    Especialidad=datos.get('especialidad', ''),
                    Horario=datos.get('horario', '')
                )
            else:
                return False, f"Tipo de trabajador no reconocido: {tipo}", None

            if not UsuarioDAO.create(nuevo_usuario):
                return False, "Error al crear la cuenta de usuario", None

            if not TrabajadorDAO.create(nuevo_usuario):
                return False, "Error al registrar el trabajador", None

            if tipo == 'auxiliar' and not AuxiliarDAO.create(nuevo_usuario):
                return False, "Error al registrar el auxiliar", None
            elif tipo == 'coordinador' and not CoordinadorDAO.create(nuevo_usuario):
                return False, "Error al registrar el coordinador", None
            elif tipo == 'especialista' and not EspecialistaDAO.create(nuevo_usuario):
                return False, "Error al registrar el especialista", None

            return True, f"Trabajador {datos['nombre_completo']} creado correctamente", nuevo_usuario

        except Exception as e:
            return False, f"Error crítico: {str(e)}", None

    @staticmethod
    def actualizar(trabajador, datos: dict) -> tuple[bool, str]:
        if 'dni' in datos and not UsuarioService.validar_dni(datos['dni']):
            return False, "DNI no válido"

        try:
            tipo = getattr(trabajador, 'tipo', None)

            nuevo_nombre   = datos.get('nombre', trabajador.nombre)
            nuevo_dni      = datos.get('dni', trabajador.dni)
            nuevo_email    = datos.get('email', trabajador.email)
            nueva_fecha    = datos.get('fechaNacimiento', trabajador.fechaNacimiento)
            nuevo_telefono = datos.get('telefono', getattr(trabajador, 'telefono', None))
            nuevo_password = datos.get('password') or trabajador.password

            common = dict(
                nombreUsuario=trabajador.nombreUsuario,
                Nombre=nuevo_nombre,
                DNI=nuevo_dni,
                password=nuevo_password,
                email=nuevo_email,
                fechaNacimiento=nueva_fecha,
                telefono=nuevo_telefono,
            )

            if tipo == 'auxiliar':
                trabajador_actualizado = Auxiliar(
                    **common,
                    Horario=getattr(trabajador, 'horario', None)
                )
            elif tipo == 'coordinador':
                trabajador_actualizado = Coordinador(
                    **common,
                    infoInteres=getattr(trabajador, 'infoInteres', None)
                )
            elif tipo == 'especialista':
                trabajador_actualizado = Especialista(
                    **common,
                    Especialidad=getattr(trabajador, 'especialidad', None),
                    Horario=getattr(trabajador, 'horario', None)
                )
            else:
                # fallback: actualizar solo la parte de Usuario
                trabajador_actualizado = trabajador
                trabajador_actualizado._nombre = nuevo_nombre
                trabajador_actualizado._dni = nuevo_dni
                trabajador_actualizado._email = nuevo_email
                trabajador_actualizado._fechaNacimiento = nueva_fecha
                trabajador_actualizado._telefono = nuevo_telefono
                trabajador_actualizado._password = nuevo_password

            exito = UsuarioDAO.update(trabajador_actualizado)
            if exito:
                return True, "Trabajador actualizado correctamente"
            return False, "Error al actualizar"
        except Exception as e:
            return False, f"Error: {str(e)}"