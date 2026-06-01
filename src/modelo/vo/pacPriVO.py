from .pacienteVO import Paciente

class PacPri(Paciente):
    #Paciente privado, tipo de paciente
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, 
                 IVA=4, cuenta=None, horas=8, email=None, activo=None):  # ← añadir activo
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            password=password,
            Tipo='privado',
            email=email,
            activo=activo  # ← pasar activo
        )
        self._iva = IVA
        self._cuenta = cuenta
        self._horas = horas

    @property
    def iva(self):
        return self._iva
    
    @property
    def cuenta(self):
        return self._cuenta
    
    @property
    def horas(self):
        return self._horas
    
    def to_dict(self):
        d = super().to_dict()
        d.update({
            'iva': self.iva,
            'cuenta': self.cuenta,
            'horas': self.horas
        })
        return d
    
    def __repr__(self):
        return f"<PacientePrivado nombreUsuario={self.nombreUsuario}>"
