from datetime import date, datetime
from app.models.usuario import Usuario

# -----------------------------------------------------
# EvaluacionProfesional
# -----------------------------------------------------

class EvaluacionProfesional:
    def __init__(self, idEvaluacion=None, Paciente=None, Trabajador=None,
                 fecha=None, movilidad=None, estadoEmocional=None,
                 apetito=None, observaciones=None):
        self._idEvaluacion = idEvaluacion
        self._paciente = Paciente
        self._trabajador = Trabajador
        self._fecha = None
        self._movilidad = movilidad
        self._estadoEmocional = estadoEmocional
        self._apetito = apetito
        self._observaciones = observaciones
        if fecha:
            self.fecha = fecha

    @property
    def idEvaluacion(self):
        return self._idEvaluacion

    @idEvaluacion.setter
    def idEvaluacion(self, value):
        self._idEvaluacion = value

    @property
    def paciente(self):
        return self._paciente

    @paciente.setter
    def paciente(self, value):
        self._paciente = value

    @property
    def trabajador(self):
        return self._trabajador

    @trabajador.setter
    def trabajador(self, value):
        self._trabajador = value

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        if value is None:
            self._fecha = None
        elif isinstance(value, date):
            self._fecha = value
        elif isinstance(value, str):
            try:
                self._fecha = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para fecha: {type(value)}")

    @property
    def movilidad(self):
        return self._movilidad

    @movilidad.setter
    def movilidad(self, value):
        self._movilidad = value

    @property
    def estadoEmocional(self):
        return self._estadoEmocional

    @estadoEmocional.setter
    def estadoEmocional(self, value):
        self._estadoEmocional = value

    @property
    def apetito(self):
        return self._apetito

    @apetito.setter
    def apetito(self, value):
        self._apetito = value

    @property
    def observaciones(self):
        return self._observaciones

    @observaciones.setter
    def observaciones(self, value):
        self._observaciones = value

    def to_dict(self):
        return {
            'idEvaluacion': self.idEvaluacion,
            'paciente': self.paciente,
            'trabajador': self.trabajador,
            'fecha': str(self.fecha) if self.fecha else None,
            'movilidad': self.movilidad,
            'estadoEmocional': self.estadoEmocional,
            'apetito': self.apetito,
            'observaciones': self.observaciones
        }

    def __repr__(self):
        return f"<EvaluacionProfesional id={self.idEvaluacion} paciente={self.paciente}>"


# -----------------------------------------------------
# Informe
# -----------------------------------------------------

class Informe:
    def __init__(self, referencia=None, Paciente=None, Trabajador=None,
                 fechaGeneracion=None, periodoInicio=None, periodoFin=None):
        self._referencia = referencia
        self._paciente = Paciente
        self._trabajador = Trabajador
        self._fechaGeneracion = None
        self._periodoInicio = None
        self._periodoFin = None
        if fechaGeneracion:
            self.fechaGeneracion = fechaGeneracion
        if periodoInicio:
            self.periodoInicio = periodoInicio
        if periodoFin:
            self.periodoFin = periodoFin

    def _parse_date(self, value, campo):
        if value is None:
            return None
        elif isinstance(value, date):
            return value
        elif isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"El formato de {campo} debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para {campo}: {type(value)}")

    @property
    def referencia(self):
        return self._referencia

    @referencia.setter
    def referencia(self, value):
        self._referencia = value

    @property
    def paciente(self):
        return self._paciente

    @paciente.setter
    def paciente(self, value):
        self._paciente = value

    @property
    def trabajador(self):
        return self._trabajador

    @trabajador.setter
    def trabajador(self, value):
        self._trabajador = value

    @property
    def fechaGeneracion(self):
        return self._fechaGeneracion

    @fechaGeneracion.setter
    def fechaGeneracion(self, value):
        self._fechaGeneracion = self._parse_date(value, 'fechaGeneracion')

    @property
    def periodoInicio(self):
        return self._periodoInicio

    @periodoInicio.setter
    def periodoInicio(self, value):
        self._periodoInicio = self._parse_date(value, 'periodoInicio')

    @property
    def periodoFin(self):
        return self._periodoFin

    @periodoFin.setter
    def periodoFin(self, value):
        self._periodoFin = self._parse_date(value, 'periodoFin')

    def to_dict(self):
        return {
            'referencia': self.referencia,
            'paciente': self.paciente,
            'trabajador': self.trabajador,
            'fechaGeneracion': str(self.fechaGeneracion) if self.fechaGeneracion else None,
            'periodoInicio': str(self.periodoInicio) if self.periodoInicio else None,
            'periodoFin': str(self.periodoFin) if self.periodoFin else None
        }

    def __repr__(self):
        return f"<Informe referencia={self.referencia} paciente={self.paciente}>"


# -----------------------------------------------------
# Factura
# -----------------------------------------------------

class Factura:
    def __init__(self, codigoFactura=None, Paciente=None, Administrador=None,
                 fechaEmision=None, importeTotal=0.00, estadoPago='pendiente'):
        self._codigoFactura = codigoFactura
        self._paciente = Paciente
        self._administrador = Administrador
        self._fechaEmision = None
        self._importeTotal = importeTotal
        self._estadoPago = estadoPago
        if fechaEmision:
            self.fechaEmision = fechaEmision

    @property
    def codigoFactura(self):
        return self._codigoFactura

    @codigoFactura.setter
    def codigoFactura(self, value):
        self._codigoFactura = value

    @property
    def paciente(self):
        return self._paciente

    @paciente.setter
    def paciente(self, value):
        self._paciente = value

    @property
    def administrador(self):
        return self._administrador

    @administrador.setter
    def administrador(self, value):
        self._administrador = value

    @property
    def fechaEmision(self):
        return self._fechaEmision

    @fechaEmision.setter
    def fechaEmision(self, value):
        if value is None:
            self._fechaEmision = None
        elif isinstance(value, date):
            self._fechaEmision = value
        elif isinstance(value, str):
            try:
                self._fechaEmision = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fechaEmision debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para fechaEmision: {type(value)}")

    @property
    def importeTotal(self):
        return self._importeTotal

    @importeTotal.setter
    def importeTotal(self, value):
        self._importeTotal = value

    @property
    def estadoPago(self):
        return self._estadoPago

    @estadoPago.setter
    def estadoPago(self, value):
        self._estadoPago = value

    def to_dict(self):
        return {
            'codigoFactura': self.codigoFactura,
            'paciente': self.paciente,
            'administrador': self.administrador,
            'fechaEmision': str(self.fechaEmision) if self.fechaEmision else None,
            'importeTotal': float(self.importeTotal),
            'estadoPago': self.estadoPago
        }

    def __repr__(self):
        return f"<Factura codigo={self.codigoFactura} paciente={self.paciente} estado={self.estadoPago}>"