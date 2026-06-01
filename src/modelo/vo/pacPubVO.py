from .pacienteVO import Paciente

class PacPub(Paciente):
    #paciente publico, tipo de paciente
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, 
                 Dias_ingresado=None, email=None, activo=None):  # ← añadir activo
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='publico',
            email=email,
            activo=activo  # ← pasar activo
        )
        self._dias_ingresado = Dias_ingresado
    
    @property
    def dias_ingresado(self):
        return self._dias_ingresado
    
    def to_dict(self):
        d = super().to_dict()
        d['dias_ingresado'] = self.dias_ingresado
        return d
    
    def __repr__(self):
        return f"<PacientePublico nombreUsuario={self.nombreUsuario} dias={self.dias_ingresado}>"