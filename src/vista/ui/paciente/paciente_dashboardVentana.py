import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType

# Cargar el archivo .ui del paciente
ui_path = os.path.join(os.path.dirname(__file__), "ui", "paciente_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def inicializar_dashboard(self, nombre_usuario: str, ya_respondio_hoy: bool):
        """
        Configura los datos dinámicos del panel del paciente.
        Simula las variables que inyectabas mediante Jinja en el HTML.
        """
        # 1. Personalizar el saludo
        self.lbl_saludo.setText(f"¡Hola, {nombre_usuario}! ¿Qué te gustaría hacer hoy?")
        
        # 2. Replicar el {% if ya_respondio_hoy %} del HTML
        if ya_respondio_hoy:
            self.lbl_ejercicio_desc.setText("¡Ya has completado el cuestionario de hoy!")
            # Le podemos dar un color verde al texto usando hojas de estilo (CSS)
            self.lbl_ejercicio_desc.setStyleSheet("color: green; font-weight: bold;")
            
            self.btn_comenzar_cuestionario.setText("Completado por hoy")
            self.btn_comenzar_cuestionario.setEnabled(False) # Deshabilitar botón
        else:
            self.lbl_ejercicio_desc.setText("Ayúdanos a saber cómo te encuentras hoy.")
            self.lbl_ejercicio_desc.setStyleSheet("color: gray;")
            
            self.btn_comenzar_cuestionario.setText("Comenzar Cuestionario")
            self.btn_comenzar_cuestionario.setEnabled(True) # Habilitar botón