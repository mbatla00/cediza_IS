from .trabajadorVO import Trabajador

class Auxiliar(Trabajador):
    #Auxiliar: tipo de trabajador

    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, Horario=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='auxiliar'
        )
        self._horario = Horario
    
    @property
    def horario(self):
        return self._horario
    
    def to_dict(self):
        d = super().to_dict()
        d['horario'] = self.horario
        return d
    
    def __repr__(self):
        return f"<Auxiliar nombreUsuario={self.nombreUsuario}>"