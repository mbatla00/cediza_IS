class Pregunta:
    """Pregunta de un cuestionario"""

    def __init__(self, idPregunta=None, idCuestionario=None, enunciado=None, tipoRespuesta=None):
        self._idPregunta = idPregunta
        self._idCuestionario = idCuestionario
        self._enunciado = enunciado
        self._tipoRespuesta = tipoRespuesta

    @property
    def idPregunta(self):
        return self._idPregunta

    @property
    def idCuestionario(self):
        return self._idCuestionario

    @property
    def enunciado(self):
        return self._enunciado

    @property
    def tipoRespuesta(self):
        return self._tipoRespuesta

    def to_dict(self):
        return {
            'idPregunta': self.idPregunta,
            'idCuestionario': self.idCuestionario,
            'enunciado': self.enunciado,
            'tipoRespuesta': self.tipoRespuesta
        }

    def __repr__(self):
        return f"<Pregunta id={self.idPregunta} cuestionario={self.idCuestionario}>"