from app.models.paciente import Paciente

class PacPub(Paciente):
    #paciente publico, con dias ingresado 
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, contraseña=None, Dias_ingresado=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            contraseña=contraseña,
            Tipo='publico'
        )
        self._dias_ingresado = Dias_ingresado
    
    @property
    def dias_ingresado(self):
        return self._dias_ingresado
    
    @dias_ingresado.setter
    def dias_ingresado(self, value):
        self._dias_ingresado = value
    
    def to_dict(self):
        d = super().to_dict()
        d['dias_ingresado'] = self.dias_ingresado
        return d
    
    def __repr__(self):
        return f"<PacPub nombreUsuario={self.nombreUsuario} dias={self.dias_ingresado}>"

class PacPri(Paciente):
    #Paciente privado con datos de facturación
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, contraseña=None, IVA=None, cuenta=None, horas=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            contraseña=contraseña,
            Tipo='privado'
        )
        self._iva = IVA
        self._cuenta = cuenta
        self._horas = horas

    @property
    def iva(self):
        return self._iva
    
    @iva.setter
    def iva(self, value):
        self._iva = value
    
    @property
    def cuenta(self):
        return self._cuenta
    
    @cuenta.setter
    def cuenta(self, value):
        self._cuenta = value
    
    @property
    def horas(self):
        return self._horas
    
    @horas.setter
    def horas(self, value):
        self._horas = value
    
    def to_dict(self):
        d = super().to_dict()
        d.update({
            'iva': self.iva,
            'cuenta': self.cuenta,
            'horas': self.horas
        })
        return d
    
    def __repr__(self):
        return f"<PacPri nombreUsuario={self.nombreUsuario}>"
        