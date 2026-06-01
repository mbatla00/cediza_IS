from .trabajadorVO import Trabajador

class Coordinador(Trabajador):
    #coordinador: tipo de trabajador

    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, 
                 infoInteres=None, activo=None):  # ← añadir activo
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='coordinador',
            activo=activo  # ← pasar activo
        ) 
        self._infoInteres = infoInteres

    @property
    def infoInteres(self):
        return self._infoInteres
    
    def to_dict(self):
        d = super().to_dict()
        d['infoInteres'] = self.infoInteres
        return d
    
    def __repr__(self):
        return f"<Coordinador nombreUsuario={self.nombreUsuario}>"