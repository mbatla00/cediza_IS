from .paciente_factory import PacienteFactory
from .trabajador_factory import TrabajadorFactory

#=====================================
# Factoria raiz
#=====================================
class UsuarioFactory:
    # Recibe un dict con un campo 'Rol' y delega en la subfactoria correspondiente

    @staticmethod
    def crear(datos:dict):
        """
        parametros esperados en 'datos':
            - Rol o Tipo: paciente | trabajador | admin
        """
        # 1. Buscamos primero en 'Rol' (que es donde viene el admin) y si no en 'Tipo'
        tipo_raw = datos.get('Rol') or datos.get('Tipo') or datos.get('tipo') or datos.get('rol')
        
        # 2. Si sigue sin encontrar nada, aplicamos los alias por si acaso
        if not tipo_raw:
            if datos.get('TipoPaciente'): tipo_raw = 'paciente'
            elif datos.get('TipoTrabajador'): tipo_raw = 'trabajador'
            elif datos.get('nombreUsuario'): tipo_raw = 'admin'

        # 3. Lo pasamos a minúsculas de forma segura
        tipo = tipo_raw.lower() if tipo_raw else ''

        # 4. Comprobamos los roles con la variable 'tipo'
        if tipo == 'paciente':
            return PacienteFactory.crear(datos)
        elif tipo == 'trabajador':
            return TrabajadorFactory.crear(datos)

        elif tipo == 'admin':
            datos_filtrados = {
                'nombreUsuario': datos.get('nombreUsuario'),
                'Nombre': datos.get('Nombre'),
                'DNI': datos.get('DNI'),
                'password': datos.get('password')
            }
            # Limpiamos valores nulos
            datos_filtrados = {k: v for k, v in datos_filtrados.items() if v is not None}
            return Admin(**datos_filtrados)

        else:
            raise ValueError(f"Rol desconocido: '{tipo}'. Valores validos: paciente, trabajador, admin")