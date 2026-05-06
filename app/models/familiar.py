class Familiar:
    def __init__(self, Nombre=None, Paciente=None, Relacion=None, Telefono=None):
        self._nombre = Nombre
        self._paciente = Paciente      #FK -> Pacientes.nombreUsuario
        self._relacion = Relacion
        self._telefono = Telefono
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value
    
    @property
    def paciente(self):
        return self._paciente
    
    @paciente.setter
    def paciente(self, value):
        self._paciente = value
    
    @property
    def relacion(self):
        return self._relacion
    
    @relacion.setter
    def relacion(self, value):
        self._relacion = value
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, value):
        self._telefono = value

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'paciente': self.paciente,
            'relacion': self.relacion,
            'telefono': self.telefono
        }
    
    def __repr__(self):
        return f"<Familiar nombre={self.nombre} paciente={self.paciente}>"