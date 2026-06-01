from .usuarioVO import Usuario

class Admin(Usuario):
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, password=None, activo=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='admin',
            password=password,
            activo=activo  # ← Pasa activo al padre
        )

    def __repr__(self):
        return f"<Admin nombreUsuario={self.nombreUsuario}>"