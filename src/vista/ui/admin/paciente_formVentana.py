import os
from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import loadUiType

# 1. Cargar el diseño
ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "trabajador_form.ui")
Ui_Dialog, _ = loadUiType(ruta_ui)

class NuevoTrabajadorVentana(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 2. Estado inicial: ocultar el campo de especialidad
        self.lbl_especialidad.setVisible(False)
        self.txt_especialidad.setVisible(False)
        
        # 3. Conectar la señal
        self.cb_tipo.currentTextChanged.connect(self.verificar_especialidad)

    def verificar_especialidad(self, texto_seleccionado):
        """Muestra u oculta la especialidad dependiendo del tipo de trabajador"""
        if texto_seleccionado.lower() == "especialista":
            self.lbl_especialidad.setVisible(True)
            self.txt_especialidad.setVisible(True)
        else:
            self.lbl_especialidad.setVisible(False)
            self.txt_especialidad.setVisible(False)
            self.txt_especialidad.clear()