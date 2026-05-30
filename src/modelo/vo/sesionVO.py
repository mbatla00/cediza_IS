class Sesion:
    """VO para una sesion entre un paciente y un especialista en un dia especifico"""
    
    def __init__(self, idSesion=None, Paciente=None, Especialista=None,
                 comentarios=None, Fecha=None, Hora=None):
        self._idSesion = idSesion
        self._paciente = Paciente
        self._especialista = Especialista
        self._comentarios = comentarios
        self._fecha = None
        self._hora = Hora
        if Fecha:
            self.fecha = Fecha

    @property
    def idSesion(self):
        return self._idSesion

    @property
    def paciente(self):
        return self._paciente
    
    @property
    def especialista(self):
        return self._especialista
    
    @property
    def comentarios(self):
        return self._comentarios
    
    @property
    def fecha(self):
        return self._fecha

    @property
    def hora(self):
        return self._hora

    def to_dict(self):
        return {
            'idSesion': self.idSesion,
            'paciente': self.paciente,
            'especialista': self.especialista,
            'comentarios': self.comentarios,
            'fecha': str(self.fecha) if self.fecha else None,
            'hora': str(self.hora) if self.hora else None
        }
    
    def __repr__(self):
        return f"<Sesion id={self.idSesion} paciente={self.paciente} especialista={self.especialista}>"