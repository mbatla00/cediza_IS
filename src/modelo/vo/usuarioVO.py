from abc import ABC, abstractmethod

class Usuario(ABC):
    #clase abstracta para todos los usuarios del sistema

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
    
    @property
    def nombre(self):
        return self._nombre

    @property
    def dni(self):
        return self._dni

    @property
    def rol(self):
        return self._rol 

    @property
    def password(self):
        return self._password

    @property
    def email(self): 
        return self._email

    @property
    def fechaNacimiento(self):
        return self._fechaNacimiento

    @property
    def activo (self):
        return self._activo
    
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