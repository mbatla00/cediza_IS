
class BaseFactory:
    @staticmethod
    def _generar_nombreUsuario(nombre:str) -> str:
        partes = nombre.strip().split()
        if len(partes)==3: # nombre, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[1]
        elif len(partes)==4: # nombre1, nombre2, apellido1, apellido2
            nombre = partes[0]
            apellido1 = partes[2]
        else:
            raise ValueError("El nombre debe ser 'Nombre (2º nombre) Apellido1 Apellido2")
        
        return f"{nombre}{apellido1}".lower()