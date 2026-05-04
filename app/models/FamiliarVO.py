class FamiliarVO:
    def __init__ (self, nombre, paciente, relacion='hij@', telefono=None):
        self.nombre = nombre
        self.paciente = paciente
        self.relacion = relacion
        self.telefono = telefono

    def __str__ (self):
        return f"Familiar: {self.nombre} - {self.paciente} - {self.relacion} - {self.telefono}"