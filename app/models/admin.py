from app.models.usuario import Usuario


class Admin(Usuario):
    """Usuario con rol de administrador del sistema"""
    
    def __init__(self, nombreUsuario=None, Nombre=None, DNI=None, contraseña=None):
        super().__init__(
            nombreUsuario=nombreUsuario,
            Nombre=Nombre,
            DNI=DNI,
            Rol='admin',
            contraseña=contraseña
        )

    def __repr__(self):
        return f"<Admin nombreUsuario={self.nombreUsuario}>"