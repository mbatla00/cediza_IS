class AuxiliarVO:
    def __init__(self, dni, nombre, horario=None):
        self.dni = dni
        self.nombre = nombre
        self.horario = horario

    def __str__(self):
        return f"Auxiliar: {self.dni} - {self.nombre} - {self.horario}"