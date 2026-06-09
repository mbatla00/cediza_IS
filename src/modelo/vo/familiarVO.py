class Familiar:
    """VO para los familiares de un paciente"""
    
    def __init__(self, idFamiliar=None, Nombre=None, Paciente=None, Relacion='hij@', Telefono=None):
        self._id = idFamiliar
        self._nombre = Nombre
        self._paciente = Paciente
        self._relacion = Relacion
        self._telefono = Telefono
    
    @property
    def id(self):
        return self._id

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
            'id': self.id,
            'nombre': self.nombre,
            'paciente': self.paciente,
            'relacion': self.relacion,
            'telefono': self.telefono
        }
    
    def __repr__(self):
        return f"<Familiar id={self.id} nombre={self.nombre} paciente={self.paciente}>"