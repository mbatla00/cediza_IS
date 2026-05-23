class Usuario:
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, Rol=None, 
    password=None, email=None, fechaNacimiento=None, activo=None):
        self._nombreUsuario = nombreUsuario
        self._nombre = Nombre
        self._dni = DNI
        self._rol = Rol 
        self._password = password
        self._email = email
        self._fechaNacimiento = fechaNacimiento
        self._activo = activo 

    
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

    @property
    def fechaNacimiento(self):
        return self._fechaNacimiento
    
    @fechaNacimiento.setter
    def fechaNacimiento(self, value):
        self._fechaNacimiento = value

    @property
    def activo (self):
        return self._activo
    
    @activo.setter
    def activo (sef, value):
        self._activo = value

    def to_dict(self):
        return {
            'nombreUsuario': self.nombreUsuario,
            'nombre': self.nombre,
            'dni': self.dni,
            'rol': self.rol,
            'email': self.email,
            'fechaNacimiento': self.fechaNacimiento,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f"<Usuario nombreUsuario={self.nombreUsuario} rol={self.rol}>"