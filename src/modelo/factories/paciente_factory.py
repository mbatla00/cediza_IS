from src.modelo.vo import pacPriVO, pacPubVO

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