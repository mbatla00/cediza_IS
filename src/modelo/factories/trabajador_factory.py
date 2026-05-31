from src.modelo.vo import Auxiliar, Coordinador, Especialista
from .base_factory import BaseFactory

#============================
#Subfactoria de Trabajadores
#============================

class TrabajadorFactory:
    #crea un subtipo de trabajador a partir de un dict de datos

    @staticmethod
    def crear(datos:dict):
        """
        Parámetros esperados en 'datos':
            -Tipo / tipo: auxiliar | coordinador | especialista
        """
        if not datos.get('nombreUsuario'):
            datos['nombreUsuario'] = BaseFactory._generar_nombreUsuario(datos.get('Nombre', ''))

        tipo_raw = datos.get('Tipo') or datos.get('tipo') or datos.get('tipoTrabajador') or datos.get('TipoTrabajador')
        
        # Deducción por campos exclusivos si es necesario
        if not tipo_raw:
            if 'Especialidad' in datos or 'especialidad' in datos:
                tipo_raw = 'especialista'
            elif 'infoInteres' in datos or 'infointeres' in datos:
                tipo_raw = 'coordinador'
            elif 'Horario' in datos or 'horario' in datos:
                tipo_raw = 'auxiliar'
            else:
                tipo_raw = ''

        tipo = str(tipo_raw).strip().lower() if tipo_raw else ''

        if tipo == 'auxiliar':
            return Auxiliar(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                Horario=datos.get('Horario')
            )
        elif tipo == 'coordinador':
            return Coordinador(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                infoInteres=datos.get('infoInteres')
            )
        elif tipo == 'especialista':
            return Especialista(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                Especialidad=datos.get('Especialidad'),
                Horario=datos.get('Horario')
            )
        else:
            # Evitamos el colapso devolviendo un subtipo por defecto si no se reconoce
            return Auxiliar(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password')
            )
