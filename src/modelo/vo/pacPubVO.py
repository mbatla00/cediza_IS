from .pacienteVO import Paciente

class PacPub(Paciente):
    #paciente publico, tipo de paciente
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, Dias_ingresado=None, email=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='publico',
            email=email
        )
        self._dias_ingresado = Dias_ingresado #Dias ingresado en hostital (para facturación)
    
    @property
    def dias_ingresado(self):
        return self._dias_ingresado
    
    
    def to_dict(self):
        d = super().to_dict()
        d['dias_ingresado'] = self.dias_ingresado
        return d
    
    def __repr__(self):
        return f"<PacientePublico nombreUsuario={self.nombreUsuario} dias={self.dias_ingresado}>"