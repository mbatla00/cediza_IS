class Informe:
    """VO para un informe de un trbajador sobre un paciente"""
    
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

    @property
    def paciente(self):
        return self._paciente

    @property
    def trabajador(self):
        return self._trabajador

    @property
    def fechaGeneracion(self):
        return self._fechaGeneracion

    @property
    def periodoInicio(self):
        return self._periodoInicio

    @property
    def periodoFin(self):
        return self._periodoFin

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