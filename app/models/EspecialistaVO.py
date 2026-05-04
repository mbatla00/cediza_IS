class EspecialistaVO:
    def __init__(self, dni, nombre, especialidad, horario=None):
        self.dni = dni 
        self.nombre = nombre 
        self.especialidad = especialidad
        self.horario = horario
    def __str__(self):
        return f"Especialista: {self.dni} - {self.nombre} - {self.especialidad} - {self.horario}"
    