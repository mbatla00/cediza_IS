"""
SERVICIO DE USUARIOS

Contiene la lógica de negocio para operaciones con usuarios.
Usa UsuarioDAO para acceder a la base de datos.
"""
from src.modelo.dao import UsuarioDAO
import re


class UsuarioService:

    @staticmethod
    def listar_activos() -> list:
        todos = UsuarioDAO.get_all()
        return [u for u in todos if getattr(u, 'activo', True)]

    @staticmethod
    def listar_todos() -> list:
        return UsuarioDAO.get_all()

    @staticmethod
    def obtener_por_nombre(nombre_usuario: str):
        return UsuarioDAO.get_by_nombreUsuario(nombre_usuario)

    @staticmethod
    def obtener_por_dni(dni: str):
        return UsuarioDAO.get_by_dni(dni)

    @staticmethod
    def validar_dni(dni: str) -> bool:
        if not re.match(r'^\d{8}[A-Za-z]$', dni):
            return False
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:-1])
        letra = dni[-1].upper()
        return letras[numero % 23] == letra

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        if not telefono:
            return True
        return bool(re.match(r'^\d{9}$', telefono))

    @staticmethod
    def actualizar(usuario, nuevos_datos: dict) -> tuple[bool, str]:
        if 'dni' in nuevos_datos and not UsuarioService.validar_dni(nuevos_datos['dni']):
            return False, "DNI no válido"

        try:
            # Acepta tanto 'fechaNacimiento' como 'fecha_nacimiento' (según quién llame)
            nueva_fecha = (
                nuevos_datos.get('fechaNacimiento') or
                nuevos_datos.get('fecha_nacimiento') or
                usuario.fechaNacimiento
            )

            nuevo_telefono = (
                nuevos_datos.get('telefono') or
                getattr(usuario, 'telefono', None)
            )

            nuevo_password = (
                nuevos_datos.get('password') or usuario.password
            )

            usuario_actualizado = type(usuario)(
                nombreUsuario=usuario.nombreUsuario,
                Nombre=nuevos_datos.get('nombre', usuario.nombre),
                DNI=nuevos_datos.get('dni', usuario.dni),
                password=nuevo_password,
                email=nuevos_datos.get('email', usuario.email),
                fechaNacimiento=nueva_fecha,
                telefono=nuevo_telefono,
            )

            exito = UsuarioDAO.update(usuario_actualizado)
            if exito:
                return True, "Usuario actualizado correctamente"
            return False, "Error al actualizar en la base de datos"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def desactivar(nombre_usuario: str) -> tuple[bool, str]:
        try:
            exito = UsuarioDAO.delete(nombre_usuario)
            if exito:
                return True, f"Usuario {nombre_usuario} desactivado correctamente"
            return False, "Error al desactivar usuario"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def activar(nombre_usuario: str) -> tuple[bool, str]:
        try:
            exito = UsuarioDAO.activar(nombre_usuario)
            if exito:
                return True, f"Usuario {nombre_usuario} reactivado correctamente"
            return False, "Error al reactivar usuario"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def crear_administrador(datos: dict) -> tuple[bool, str]:
        from src.modelo.vo import Admin
        from src.modelo.dao import AdministradorDAO

        if not datos.get('nombre_completo') or not datos.get('nombre_usuario'):
            return False, "Nombre completo y nombre de usuario son obligatorios"

        if not UsuarioService.validar_dni(datos.get('dni', '')):
            return False, "DNI no válido"

        if datos.get('telefono') and not UsuarioService.validar_telefono(datos['telefono']):
            return False, "Teléfono no válido (deben ser 9 dígitos)"

        if UsuarioDAO.get_by_nombreUsuario(datos['nombre_usuario']):
            return False, f"El nombre de usuario {datos['nombre_usuario']} ya existe"

        if UsuarioDAO.get_by_dni(datos['dni']):
            return False, f"Ya existe un usuario con DNI {datos['dni']}"

        try:
            nuevo_admin = Admin(
                nombreUsuario=datos['nombre_usuario'],
                Nombre=datos['nombre_completo'],
                DNI=datos['dni'],
                password=datos.get('password', datos['dni']),
                email=datos.get('email'),
                fechaNacimiento=datos.get('fecha_nacimiento'),
                telefono=datos.get('telefono'),
            )

            if not UsuarioDAO.create(nuevo_admin):
                return False, "Error al crear la cuenta de administrador"

            if not AdministradorDAO.create(nuevo_admin):
                return False, "Error al crear registro de administrador"

            return True, f"Administrador {datos['nombre_completo']} creado correctamente"
        except Exception as e:
            return False, f"Error crítico: {str(e)}"
        
        
    @staticmethod
    def cambiar_estado(nombre_usuario: str, activar_usuario: bool) -> tuple[bool, str]:
        if activar_usuario:
            exito = UsuarioDAO.activar(nombre_usuario)
            msg = f"El usuario '{nombre_usuario}' ha sido ACTIVADO (dado de alta)."
        else:
            exito = UsuarioDAO.delete(nombre_usuario)
            msg = f"El usuario '{nombre_usuario}' ha sido DESACTIVADO (dado de baja)."
        
        return exito, msg