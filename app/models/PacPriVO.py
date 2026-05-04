class PacPriVO:
    def __init__ (self, dni, nombre, iva=4, cuenta=None, horas=8):
        self.dni = dni
        self.nombre = nombre
        self.iva = iva
        self.cuenta = cuenta
        self.horas = horas
    def __str__(self):
        return f"Paciente Privado: {self.dni} - {self.nombre} - IVA:{self.iva} - {self.cuenta} - {self.horas}h"