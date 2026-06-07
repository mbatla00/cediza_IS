from abc import ABC
from .usuarioVO import Usuario

class Trabajador(Usuario, ABC):
    """VO para trabajadores del centro de dia (tipo de usuarios)"""

    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None,
                 Tipo=None, email=None, fechaNacimiento=None, telefono=None, activo=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='trabajador',
            password=password,
            email=email,
            fechaNacimiento=fechaNacimiento,
            activo=activo
        )
        self._tipo = Tipo
        self._telefono = telefono

    @property
    def tipo(self):
        return self._tipo

    @property
    def telefono(self):
        return self._telefono

    def to_dict(self):
        d = super().to_dict()
        d['tipo'] = self.tipo
        d['telefono'] = self.telefono
        return d

    def __repr__(self):
        return f"<Trabajador nombreUsuario={self.nombreUsuario} tipo={self.tipo}>"