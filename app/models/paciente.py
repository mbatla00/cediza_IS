from app.models.usuario import Usuario

class Paciente(Usuario):
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password='paciente', Tipo=None, email=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='paciente',
            password=password,
            email=email
        )
        self._tipo = Tipo #'publico' | 'privado'
    
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
        return f"<Paciente nombreUsuario={self.nombreUsuario} tipo={self.tipo}>"
