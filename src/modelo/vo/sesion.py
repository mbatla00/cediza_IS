from datetime import date, datetime, time

class Sesion:
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
        if value is None:
            self._fecha = None
        elif isinstance(value, date):
            self._fecha = value
        elif isinstance(value, str):
            try:
                self._fecha = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de fecha debe ser 'YYYY-MM-DD'")
        else:
            raise TypeError(f"Tipo no válido para fecha: {type(value)}")

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, value):
        if value is None:
            self._hora = None
        elif isinstance(value, time):
            self._hora = value
        elif isinstance(value, str):
            try:
                self._hora = datetime.strptime(value, "%H:%M:%S").time()
            except ValueError:
                try:
                    self._hora = datetime.strptime(value, "%H:%M").time()
                except ValueError:
                    raise ValueError("El formato de hora debe ser 'HH:MM:SS' o 'HH:MM'")
        else:
            self._hora = value
    
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