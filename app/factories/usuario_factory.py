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