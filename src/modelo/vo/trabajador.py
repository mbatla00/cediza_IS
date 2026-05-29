from .usuario import Usuario

class Trabajador(Usuario):
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, Tipo=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='trabajador',
            password=password
        )
        self._tipo = Tipo # 'auxiliar' | 'coordinador' | 'especialista'
    
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    def to_dict(self):
        d = super().to_dict()
        d['tipo'] = self.tipo
        return d
    
    def __repr__(self):
        return f"<Trabajador nombreUsuario={self.nombreUsuario} tipo={self.tipo}>"