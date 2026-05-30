class Respuesta:
    """VO para una respuesta a una pregunta por un paciente (para los cuestionarios) """
    
    def __init__(self, idRespuesta=None, idPregunta=None, idPaciente=None,
                 fechaHora=None, contenido=None):
        self._idRespuesta = idRespuesta
        self._idPregunta = idPregunta
        self._idPaciente = idPaciente
        self._fechaHora = None
        self._contenido = contenido
        if fechaHora:
            self.fechaHora = fechaHora

    @property
    def idRespuesta(self):
        return self._idRespuesta

    @property
    def idPregunta(self):
        return self._idPregunta

    @property
    def idPaciente(self):
        return self._idPaciente

    @property
    def fechaHora(self):
        return self._fechaHora

    @property
    def contenido(self):
        return self._contenido

    def to_dict(self):
        return {
            'idRespuesta': self.idRespuesta,
            'idPregunta': self.idPregunta,
            'idPaciente': self.idPaciente,
            'fechaHora': str(self.fechaHora) if self.fechaHora else None,
            'contenido': self.contenido
        }

    def __repr__(self):
        return f"<Respuesta id={self.idRespuesta} paciente={self.idPaciente} pregunta={self.idPregunta}>"