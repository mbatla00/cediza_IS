from app.models.paciente_tipos import PacPub, PacPri
from app.models.trabajador_tipos import Auxiliar, Coordinador, Especialista
from app.models.admin import Admin

#===========================
#Subfactoria de Pacientes
#===========================

class PacienteFactory:
    #crea el subtipo correcto de Paciente a partir de un dict de datos

    @staticmethod
    def crear(datos: dict):
        """
        Parámetros esperados en 'datos':
            - Tipo / tipo: 'publico' | 'privado'
        """
        if not datos.get('nombreUsuario'):
            datos['nombreUsuario'] = UsuarioFactory._generar_nombreUsuario(datos.get('Nombre', ''))

        # CLÁUSULA DE ULTRA-PROTECCIÓN: Buscamos todas las variantes posibles
        tipo_raw = datos.get('Tipo') or datos.get('tipo') or datos.get('tipoPaciente') or datos.get('TipoPaciente')
        
        # Si sigue sin aparecer el tipo, lo deducimos por sus propiedades exclusivas
        if not tipo_raw:
            if 'Dias_ingresado' in datos or 'dias_ingresado' in datos or 'Dias_ingresado' in datos.keys():
                tipo_raw = 'publico'
            elif 'cuenta' in datos or 'iva' in datos or 'IVA' in datos:
                tipo_raw = 'privado'
            else:
                # Si llega de una consulta de la BD limpia, miramos si tiene alias asignados
                tipo_raw = ''

        tipo = str(tipo_raw).strip().lower() if tipo_raw else ''

        if tipo == 'publico':
            return PacPub(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                Dias_ingresado=datos.get('Dias_ingresado') if datos.get('Dias_ingresado') is not None else 0,
                email=datos.get('email')
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
                email=datos.get('email')
            )
        else:
            # Si a pesar de todo no sabemos qué es, devolvemos un Paciente genérico 
            # para que la inserción o validación en el DAO NO EXPLOTE
            return PacPub(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                password=datos.get('password'),
                email=datos.get('email')
            )


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
            datos['nombreUsuario'] = UsuarioFactory._generar_nombreUsuario(datos.get('Nombre', ''))

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
#=====================================
# Factoria raiz
#=====================================
class UsuarioFactory:
    # Recibe un dict con un campo 'Rol' y delega en la subfactoria correspondiente

    @staticmethod
    def _generar_nombreUsuario(nombre:str) -> str:
        partes = nombre.strip().split()
        if len(partes)==3: # nombre, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[1]
        elif len(partes)==4: # nombre1, nombre2, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[2]
        else:
            raise ValueError("El nombre debe ser 'Nombre (2º nombre) Apellido1 Apellido2")
        
        return f"{nombre}{apellido1}".lower()


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