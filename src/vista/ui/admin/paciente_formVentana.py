import os
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class NuevoPacienteVentana(QDialog):
    def __init__(self):
        super().__init__()
        
        # 1. Construir la ruta relativa al archivo .ui
        ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "paciente_form.ui")
        
        # 2. Cargar la interfaz del formulario
        loadUi(ruta_ui, self)
        
        # 3. Configuraciones adicionales (opcionales pero útiles)
        # Ajustar la tabla de contactos (Familiares) para que se vea bien
        self.Familiares.horizontalHeader().setStretchLastSection(True)
        
        # Ocultar la cuenta bancaria por defecto si seleccionamos "Público" al inicio
        self.text_Cuenta_Bancaria.setVisible(False)
        self.label_9.setVisible(False) # Asumiendo que label_9 es "Cuenta bancaria"