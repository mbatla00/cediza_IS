from abc import ABC, abstractmethod
from .usuarioVO import Usuario

class Trabajador(Usuario, ABC):
    """VO para trabajadores del centro de dia (tipo de usuarios)"""

    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, 
                 Tipo=None, activo=None):  # ← añadir activo
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='trabajador',
            password=password,
            activo=activo  # ← pasar activo
        )
        self._tipo = Tipo
    
    @property
    def tipo(self):
        return self._tipo

    def to_dict(self):
        d = super().to_dict()
        d['tipo'] = self.tipo
        return d
    
    def __repr__(self):
        return f"<Trabajador nombreUsuario={self.nombreUsuario} tipo={self.tipo}>"