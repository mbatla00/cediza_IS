class Comentario:
    def __init__(self, Auxiliar=None, Paciente=None, dia=None, nota=None):
        self._auxiliar = Auxiliar        #FK -> Trabajadores.nombreUsuario
        self._paciente = Paciente        #FK -> Pacientes.nombreUsuario
        self._dia = dia
        self._nota = nota

    @property
    def auxiliar(self):
        return self._auxiliar
    
    @auxiliar.setter
    def auxiliar(self, value):
        self._auxiliar = value
    
    @property
    def paciente(self):
        return self._paciente

    @paciente.setter
    def paciente(self, value):
        self._paciente = value
    
    @property
    def dia(self):
        return self._dia
    
    
    from datetime import date, datetime

    @dia.setter
    def dia(self, value):
        if value is None:
            self._dia = None
        elif isinstance(value, date):
            self._dia = value
        elif isinstance(value, str):
            try:
                self._dia = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para dia: {type(value)}")

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, value):
        self._nota = value

    def to_dict(self):
        return {
            'auxiliar': self.auxiliar,
            'paciente': self.paciente,
            'dia': str(self.dia) if self.dia else None,
            'nota': self.nota
        }
    
    def __repr__(self):
        return f"<Comentario auxiliar={self.auxiliar} paciente={self.paciente} dia={self.dia}>"