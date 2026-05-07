from app.models.paciente_tipos import PacPub, PacPri
from app.models.trabajador_tipos import Auxiliar, Coordinador, Especialista

#===========================
#Subfactoria de Pacientes
#===========================

class PacienteFactory:
    #crea el subtipo correcto de Paciente a partir de un dict de datos

    @staticmethod
    def crear(datos: dict):
        """
        Parámetros esperados en 'datos':
            - Tipo: 'publico' | 'privado'
            -nombreUsuario, Nombre, DNI, contraseña
            -(PacPub) Dias_ingresado
            -(PacPri) IVA, cuenta, horas
        """
        if not datos.get('nombreUsuario'):
            datos['nombreUsuario'] = UsuarioFactory._generar_nombreUsuario(datos.get('Nombre', ''))

        tipo = datos.get('Tipo', '').lower()

        if tipo == 'publico':
            return PacPub(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                contraseña=datos.get('contraseña'),
                Dias_ingresado=datos.get('Dias_ingresado')
            )
        elif tipo == 'privado':
            return PacPri(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                contraseña=datos.get('contraseña'),
                IVA=datos.get('IVA'),
                cuenta=datos.get('cuenta'),
                horas=datos.get('horas')
            )
        else:
            raise ValueError(f"Tipo de paciente desconocido: {tipo}. Valores permitidos: publico, privado.")


#============================
#Subfactoria de Trabajadores
#============================

class TrabajadorFactory:
    #crea un subtipo de trabajador a partir de un dict de datos

    @staticmethod
    def crear(datos:dict):
        """
        Parámetros esperados en 'datos':
            -Tipo: auxiliar | coordinador | especialista
            -nombreUsuario, Nombre, DNI, contraseña
            -(Auxiliar) Horario
            -(coordinador) infoInteres
            -(Especialista) Especialidad, Horario
        """
        if not datos.get('nombreUsuario'):
            datos['nombreUsuario'] = UsuarioFactory._generar_nombreUsuario(datos.get('Nombre', ''))

        tipo = datos.get('Tipo', '').lower()

        if tipo == 'auxiliar':
            return Auxiliar(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                contraseña=datos.get('contraseña'),
                Horario=datos.get('Horario')
            )
        elif tipo == 'coordinador':
            return Coordinador(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                contraseña=datos.get('contraseña'),
                infoInteres=datos.get('infoInteres')
            )
        elif tipo == 'especialista':
            return Especialista(
                nombreUsuario=datos.get('nombreUsuario'),
                Nombre=datos.get('Nombre'),
                DNI=datos.get('DNI'),
                contraseña=datos.get('contraseña'),
                Especialidad=datos.get('Especialidad'),
                Horario=datos.get('Horario')
            )
        else:
            raise ValueError(f"Tipo de trabajador desconocido: {tipo}. Valores validos: auxiliar, coordinador, especialista.")

#=====================================
#Factoria raiz
#=====================================
class UsuarioFactory:
    #Recibe un dict con un campo 'Rol' y delega en la subfactoria correspondiente

    @staticmethod
    def _generar_nombreUsuario(nombre:str) -> str:
        partes = nombre.strip().split()
        if len(partes)==3: #nombre, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[1]
        elif len(partes)==4: #nombre1, nombre2, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[2]
        else:
            raise ValueError("El nombre debe ser 'Nombre (2º nombre) Apellido1 Apellido2")
        
        return f"{apellido1}{nombre}"


    @staticmethod
    def crear(datos:dict):
        """
        parametros esperados en 'datos':
            -Rol: paciente | trabajador
            -... (el resto segun el subtipo)
        """
        rol = datos.get('Rol', '').lower()

        if rol == 'paciente':
            return PacienteFactory.crear(datos)
        elif rol=='trabajador':
            return TrabajadorFactory.crear(datos)
        else:
            raise ValueError(f"Rol desconocido: {rol}. Valores validos: paciente, trabajador")
