class Usuario:
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, Rol=None, password=None, email=None, fechaNacimiento=None):
        self._nombreUsuario = nombreUsuario
        self._nombre = Nombre
        self._dni = DNI
        self._rol = Rol 
        self._password = password
        self._email = email 
        self.fechaNacimiento = fechaNacimiento

    
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
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self): 
        return self._email
    
    @email.setter
    def email(self, value): 
        self._email = value

    def to_dict(self):
        return {
            'nombreUsuario': self.nombreUsuario,
            'nombre': self.nombre,
            'dni': self.dni,
            'rol': self.rol,
            'email': self.email
        }
    
    def __repr__(self):
        return f"<Usuario nombreUsuario={self.nombreUsuario} rol={self.rol}>"