from datetime import date, datetime

class Comentario:
    def __init__(self, id=None, Auxiliar=None, Paciente=None, dia=None, hora=None, nota=None):
        self._id = id
        self._auxiliar = Auxiliar        # FK -> Trabajadores.nombreUsuario
        self._paciente = Paciente        # FK -> Pacientes.nombreUsuario
        self._dia = None
        self._hora = hora
        self._nota = nota
        if dia:
            self.dia = dia

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

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
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, value):
        self._hora = value

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, value):
        self._nota = value

    def to_dict(self):
        return {
            'id': self.id,
            'auxiliar': self.auxiliar,
            'paciente': self.paciente,
            'dia': str(self.dia) if self.dia else None,
            'hora': str(self.hora) if self.hora else None,
            'nota': self.nota
        }
    
    def __repr__(self):
        return f"<Comentario id={self.id} auxiliar={self.auxiliar} paciente={self.paciente} dia={self.dia}>"