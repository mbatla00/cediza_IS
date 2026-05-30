class Cuestionario:
    """VO para cuestionarios realizados a los pacientes"""
    
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

    @property
    def titulo(self):
        return self._titulo

    @property
    def tipo(self):
        return self._tipo

    @property
    def fechaAsignacion(self):
        return self._fechaAsignacion

    def to_dict(self):
        return {
            'idCuestionario': self.idCuestionario,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'fechaAsignacion': str(self.fechaAsignacion) if self.fechaAsignacion else None
        }

    def __repr__(self):
        return f"<Cuestionario id={self.idCuestionario} titulo={self.titulo}>"
