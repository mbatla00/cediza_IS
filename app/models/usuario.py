class Usuario:
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, Rol=None, contraseña=None):
        self._nombreUsuario = nombreUsuario
        self._nombre = Nombre
        self._dni = DNI
        self._rol = Rol 
        self._contraseña = contraseña

    
    @property
    def nombreUsuario(self):
        return self._nombreUsuario
    
    @nombreUsuario.setter
    def nombreUsuario (self, value):
        self._nombreUsuario = value
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def dni(self):
        return self._dni
    
    @dni.setter
    def dni(self, value):
        self._dni = value
    
    @property
    def rol(self):
        return self._rol 
    
    @rol.setter
    def rol(self, value):
        self._rol = value

    @property
    def contraseña(self):
        return self._contraseña
    
    @contraseña.setter
    def contraseña(self, value):
        self._contraseña = value

    def to_dict(self):
        return {
            'nombreUsuario': self.nombreUsuario,
            'nombre': self.nombre,
            'dni': self.dni,
            'rol': self.rol
        }
    
    def __repr__(self):
        return f"<Usuario nombreUsuario={self.nombreUsuario} rol={self.rol}>"