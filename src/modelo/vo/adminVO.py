from .usuarioVO import Usuario

class Admin(Usuario):
    # Tipo de usuario con todos los permisos
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None,
                 email=None, fechaNacimiento=None, telefono=None, activo=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='admin',
            password=password,
            email=email,
            fechaNacimiento=fechaNacimiento,
            telefono=telefono,
            activo=activo
        )

    def __repr__(self):
        return f"<Admin nombreUsuario={self.nombreUsuario}>"