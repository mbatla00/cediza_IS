import os
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class LoginVentana(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Construir la ruta al archivo .ui (evita errores si ejecutas desde otra carpeta)
        # Asumiendo que Login.ui está en la carpeta 'ui' al lado de este script
        ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "login.ui")
        
        # 2. Cargar la interfaz visual
        loadUi(ruta_ui, self)
        
        # 3. Configuraciones extra 
        # oculatmos contraseña en xml
        from PyQt6.QtWidgets import QLineEdit
        self.entradaContrasena.setEchoMode(QLineEdit.EchoMode.Password)