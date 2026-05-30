class Comentario:
    """VO para comentarios de un trabajador a un paciente en un dia y hora determinados"""
    
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

    @property
    def auxiliar(self):
        return self._auxiliar
    
    @property
    def paciente(self):
        return self._paciente

    @property
    def dia(self):
        return self._dia

    @property
    def hora(self):
        return self._hora

    @property
    def nota(self):
        return self._nota

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