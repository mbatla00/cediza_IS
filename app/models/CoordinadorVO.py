class CoordinadorVO:
    def __init__(self, dn, nombre):
        self.dn = dn
        self.nombre = nombre
    
    def __str__ (self):
        return f"Coordinador: {self.dn} - {self.nombre}"