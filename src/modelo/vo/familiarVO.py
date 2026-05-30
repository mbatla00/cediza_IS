class Familiar:
    """VO para los familiares de un paciente"""
    
    def __init__(self, Nombre=None, Paciente=None, Relacion='hij@', Telefono=None):
        self._nombre = Nombre
        self._paciente = Paciente      #FK -> Pacientes.nombreUsuario
        self._relacion = Relacion
        self._telefono = Telefono
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def paciente(self):
        return self._paciente
    
    @property
    def relacion(self):
        return self._relacion
    
    @property
    def telefono(self):
        return self._telefono

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'paciente': self.paciente,
            'relacion': self.relacion,
            'telefono': self.telefono
        }
    
    def __repr__(self):
        return f"<Familiar nombre={self.nombre} paciente={self.paciente}>"