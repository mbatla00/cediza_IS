from src.modelo.vo import PacPri, PacPub
from .base_factory import BaseFactory


class PacienteFactory:

    @staticmethod
    def crear(datos: dict):
        if not datos.get('nombreUsuario'):
            datos['nombreUsuario'] = BaseFactory._generar_nombreUsuario(datos.get('Nombre', ''))

        # Obtener activo
        activo = datos.get('activo') or datos.get('Activo')
        if activo is not None:
            activo = 1 if activo in (1, True, '1', 'true', 'True') else 0

        tipo_raw = datos.get('Tipo') or datos.get('tipo') or datos.get('tipoPaciente') or datos.get('TipoPaciente')
        
        if not tipo_raw:
            if 'Dias_ingresado' in datos or 'dias_ingresado' in datos:
                tipo_raw = 'publico'
            elif 'cuenta' in datos or 'iva' in datos or 'IVA' in datos:
                tipo_raw = 'privado'
            else:
                tipo_raw = ''

        tipo = str(tipo_raw).strip().lower() if tipo_raw else ''

        if tipo == 'publico':
            return PacPub(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                Dias_ingresado=datos.get('Dias_ingresado') if datos.get('Dias_ingresado') is not None else 0,
                email=datos.get('email'),
                activo=activo  # ← añadir activo
            )
        elif tipo == 'privado':
            return PacPri(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                IVA=datos.get('IVA') if datos.get('IVA') is not None else 4,
                cuenta=datos.get('cuenta'),
                horas=datos.get('horas') if datos.get('horas') is not None else 8,
                email=datos.get('email'),
                activo=activo  # ← añadir activo
            )
        else:
            return PacPub(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                email=datos.get('email'),
                activo=activo  # ← añadir activo
            )