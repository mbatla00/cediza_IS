from .trabajador import Trabajador

class Auxiliar(Trabajador):
    #Auxiliar: tiene horario asignado

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
    
    @horario.setter
    def horario(self, value):
        self._horario = value
    
    def to_dict(self):
        d = super().to_dict()
        d['horario'] = self.horario
        return d
    
    def __repr__(self):
        return f"<Auxiliar nombreUsuario={self.nombreUsuario}>"
    
class Coordinador(Trabajador):
    #coordinador: tiene info de interes

    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, infoInteres=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='coordinador'
        ) 
        self._infoInteres = infoInteres

    @property
    def infoInteres(self):
        return self._infoInteres
    
    @infoInteres.setter
    def infoInteres(self, value):
        self._infoInteres = value
    
    def to_dict(self):
        d = super().to_dict()
        d['infoInteres'] = self.infoInteres
        return d
    
    def __repr__(self):
        return f"<Coordinador nombreUsuario={self.nombreUsuario}>"

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
    
    @especialidad.setter
    def especialidad(self, value):
        self._especialidad = value

    @property
    def horario(self):
        return self._horario
    
    @horario.setter
    def horario(self, value):
        self._horario = value
    
    def to_dict(self):
        d = super().to_dict()
        d.update({
            'especialidad': self.especialidad,
            'horario': self.horario
        })
        return d
    
    def __repr__(self):
        return f"<Especialista nombreUsuario={self.nombreUsuario} especialidad={self.especialidad}>"