from .paciente_factory import PacienteFactory
from .trabajador_factory import TrabajadorFactory
from src.modelo.vo import Admin


class UsuarioFactory:

    @staticmethod
    def crear(datos: dict):
        tipo_raw = datos.get('Rol') or datos.get('Tipo') or datos.get('tipo') or datos.get('rol')
        
        if not tipo_raw:
            if datos.get('TipoPaciente'):
                tipo_raw = 'paciente'
            elif datos.get('TipoTrabajador'):
                tipo_raw = 'trabajador'
            elif datos.get('nombreUsuario'):
                tipo_raw = 'admin'

        tipo = tipo_raw.lower() if tipo_raw else ''

        # Obtener activo de los datos
        activo = datos.get('activo') or datos.get('Activo')
        if activo is not None:
            activo = 1 if activo in (1, True, '1', 'true', 'True') else 0

        if tipo == 'paciente':
            return PacienteFactory.crear(datos)
        elif tipo == 'trabajador':
            return TrabajadorFactory.crear(datos)
        elif tipo == 'admin':
            datos_filtrados = {
                'nombreUsuario': datos.get('nombreUsuario'),
                'Nombre': datos.get('Nombre'),
                'DNI': datos.get('DNI'),
                'password': datos.get('password'),
                'activo': activo  # ← Esto pasa activo en el CONSTRUCTOR
            }
            datos_filtrados = {k: v for k, v in datos_filtrados.items() if v is not None}
            return Admin(**datos_filtrados)  # ← Admin recibe activo en __init__
        else:
            raise ValueError(f"Rol desconocido: '{tipo}'")