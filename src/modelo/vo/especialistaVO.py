from .trabajadorVO import Trabajador

class Especialista(Trabajador):
    #Especialista: tiene una especialidad y horario
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, Especialidad=None, Horario=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='especialista'
        )
        self._especialidad = Especialidad
        self._horario = Horario
    
    @property
    def especialidad(self):
        return self._especialidad

    @property
    def horario(self):
        return self._horario
    
    def to_dict(self):
        d = super().to_dict()
        d.update({
            'especialidad': self.especialidad,
            'horario': self.horario
        })
        return d
    
    def __repr__(self):
        return f"<Especialista nombreUsuario={self.nombreUsuario} especialidad={self.especialidad}>"