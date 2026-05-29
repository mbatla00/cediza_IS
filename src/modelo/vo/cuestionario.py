from datetime import datetime


class Cuestionario:
    def __init__(self, idCuestionario=None, titulo=None, tipo=None, fechaAsignacion=None):
        self._idCuestionario = idCuestionario
        self._titulo = titulo
        self._tipo = tipo
        self._fechaAsignacion = None
        if fechaAsignacion:
            self.fechaAsignacion = fechaAsignacion

    @property
    def idCuestionario(self):
        return self._idCuestionario

    @idCuestionario.setter
    def idCuestionario(self, value):
        self._idCuestionario = value

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def fechaAsignacion(self):
        return self._fechaAsignacion

    @fechaAsignacion.setter
    def fechaAsignacion(self, value):
        from datetime import date
        if value is None:
            self._fechaAsignacion = None
        elif isinstance(value, date):
            self._fechaAsignacion = value
        elif isinstance(value, str):
            try:
                self._fechaAsignacion = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para fechaAsignacion: {type(value)}")

    def to_dict(self):
        return {
            'idCuestionario': self.idCuestionario,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'fechaAsignacion': str(self.fechaAsignacion) if self.fechaAsignacion else None
        }

    def __repr__(self):
        return f"<Cuestionario id={self.idCuestionario} titulo={self.titulo}>"


class Pregunta:
    def __init__(self, idPregunta=None, idCuestionario=None, enunciado=None, tipoRespuesta=None):
        self._idPregunta = idPregunta
        self._idCuestionario = idCuestionario
        self._enunciado = enunciado
        self._tipoRespuesta = tipoRespuesta

    @property
    def idPregunta(self):
        return self._idPregunta

    @idPregunta.setter
    def idPregunta(self, value):
        self._idPregunta = value

    @property
    def idCuestionario(self):
        return self._idCuestionario

    @idCuestionario.setter
    def idCuestionario(self, value):
        self._idCuestionario = value

    @property
    def enunciado(self):
        return self._enunciado

    @enunciado.setter
    def enunciado(self, value):
        self._enunciado = value

    @property
    def tipoRespuesta(self):
        return self._tipoRespuesta

    @tipoRespuesta.setter
    def tipoRespuesta(self, value):
        self._tipoRespuesta = value

    def to_dict(self):
        return {
            'idPregunta': self.idPregunta,
            'idCuestionario': self.idCuestionario,
            'enunciado': self.enunciado,
            'tipoRespuesta': self.tipoRespuesta
        }

    def __repr__(self):
        return f"<Pregunta id={self.idPregunta} cuestionario={self.idCuestionario}>"


class Respuesta:
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

    @idRespuesta.setter
    def idRespuesta(self, value):
        self._idRespuesta = value

    @property
    def idPregunta(self):
        return self._idPregunta

    @idPregunta.setter
    def idPregunta(self, value):
        self._idPregunta = value

    @property
    def idPaciente(self):
        return self._idPaciente

    @idPaciente.setter
    def idPaciente(self, value):
        self._idPaciente = value

    @property
    def fechaHora(self):
        return self._fechaHora

    @fechaHora.setter
    def fechaHora(self, value):
        if value is None:
            self._fechaHora = None
        elif isinstance(value, datetime):
            self._fechaHora = value
        elif isinstance(value, str):
            try:
                self._fechaHora = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("El formato de fechaHora debe ser 'YYYY-MM-DD HH:MM:SS'")
        else:
            raise TypeError(f"Tipo no válido para fechaHora: {type(value)}")

    @property
    def contenido(self):
        return self._contenido

    @contenido.setter
    def contenido(self, value):
        self._contenido = value

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