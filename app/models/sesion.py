class Sesion:
    def __init__(self, idSesion=None, Paciente=None, Especialista=None,
    comentarios=None, Fecha=None):
        self._idSesion = idSesion
        self._paciente = Paciente    #FK -> Pacientes.nombreUsuario
        self._especialista = Especialista   #FK -> Especialistas.nombreUsuario
        self._comentarios = comentarios
        self._fecha = Fecha

    @property
    def idSesion(self):
        return self._idSesion
    
    @idSesion.setter
    def idSesion(self, value):
        self._idSesion = value

    @property
    def paciente(self):
        return self._paciente
    
    @paciente.setter
    def paciente(self, value):
        self._paciente = value
    
    @property
    def especialista(self):
        return self._especialista

    @especialista.setter
    def especialista(self, value):
        self._especialista = value
    
    @property
    def comentarios(self):
        return self._comentarios
    
    @comentarios.setter
    def comentarios(self, value):
        self._comentarios = value
    
    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        self._fecha = value
    
    def to_dict(self):
        return {
            'idSesion': self.idSesion,
            'paciente': self.paciente,
            'especialista': self.especialista,
            'comentarios': self.comentarios,
            'fecha': str(self.fecha) if self.fecha else None
        }
    
    def __repr__(self):
        return f"<Sesion id={self.idSesion} paciente={self.paciente} especialista={self.especialista}>"
