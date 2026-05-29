from .usuario import Usuario

class Paciente(Usuario):
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password='paciente',
    Tipo=None, email=None, fechaNacimiento=None, activo=None, diagnostico=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='paciente',
            password=password,
            email=email,
            fechaNacimiento=fechaNacimiento,
            activo=activo
        )
        self._tipo = Tipo #'publico' | 'privado'
        self._diagnostico = diagnostico
    
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, value):
        self._tipo = value
    
    @property
    def diagnostico(self):
        return self._diagnostico
    
    @diagnostico.setter
    def diagnostico (self, value):
        self._diagnostico = value
    
    def to_dict(self):
        d = super().to_dict()
        d['tipo'] = self.tipo
        d['diagnostico']=self.diagnostico
        return d
    
    def __repr__(self):
        return f"<Paciente nombreUsuario={self.nombreUsuario} tipo={self.tipo}>"
