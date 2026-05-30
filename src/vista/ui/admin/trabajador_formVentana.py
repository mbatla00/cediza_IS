import os
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class NuevoTrabajadorVentana(QDialog):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar el diseño
        ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "trabajador_form.ui")
        loadUi(ruta_ui, self)
        
        # 2. Estado inicial: ocultar el campo de especialidad por defecto
        self.lbl_especialidad.setVisible(False)
        self.txt_especialidad.setVisible(False)
        
        # 3. Conectar la señal de cambio del combobox a nuestra función visual
        self.cb_tipo.currentTextChanged.connect(self.verificar_especialidad)

    def verificar_especialidad(self, texto_seleccionado):
        """Muestra u oculta la especialidad dependiendo del tipo de trabajador"""
        if texto_seleccionado.lower() == "especialista":
            self.lbl_especialidad.setVisible(True)
            self.txt_especialidad.setVisible(True)
        else:
            self.lbl_especialidad.setVisible(False)
            self.txt_especialidad.setVisible(False)
            self.txt_especialidad.clear()  # Limpiamos el texto por si habían escrito algo