class EvaluacionProfesional:
    """VO para la evaluación de un trabajador a un paciente """
    
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

    @property
    def paciente(self):
        return self._paciente

    @property
    def trabajador(self):
        return self._trabajador

    @property
    def fecha(self):
        return self._fecha

    @property
    def movilidad(self):
        return self._movilidad

    @property
    def estadoEmocional(self):
        return self._estadoEmocional

    @property
    def apetito(self):
        return self._apetito

    @property
    def observaciones(self):
        return self._observaciones

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
