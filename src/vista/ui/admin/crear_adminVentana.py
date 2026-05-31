import os
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtUiTools import loadUiType

# 1. Carga el archivo .ui al estilo oficial de PySide6
ui_file = os.path.join(os.path.dirname(__file__), "ui", "crear_admin.ui")
ui_formulario, _ = loadUiType(ui_file)

class CrearAdminVentana(QDialog, ui_formulario):
    def __init__(self):
        super().__init__()
        
        # 2. Inicializa y dibuja la interfaz en 'self'
        self.setupUi(self)
        
        # 3. Restricciones visuales (Validadores en la Vista)
        self.configurar_restricciones()

    def configurar_restricciones(self):
        """Aplica filtros para que el usuario no escriba datos basura"""
        
        # El teléfono solo puede tener números (9 dígitos)
        regex_tel = QRegularExpression(r"^\d{0,9}$")
        validador_tel = QRegularExpressionValidator(regex_tel, self)
        self.txt_telefono.setValidator(validador_tel)
        
        # El DNI obliga a meter 8 números y una letra (fuerza mayúsculas en el controlador)
        regex_dni = QRegularExpression(r"^\d{0,8}[a-zA-Z]?$")
        validador_dni = QRegularExpressionValidator(regex_dni, self)
        self.txt_dni.setValidator(validador_dni)