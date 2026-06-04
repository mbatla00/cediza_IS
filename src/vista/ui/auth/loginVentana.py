import os
from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtUiTools import loadUiType

# 1. Cargamos el archivo .ui de forma dinámica
ui_path = os.path.join(os.path.dirname(__file__), "login.ui") 
# (Nota: si tu login.ui está dentro de una carpeta "ui", cámbialo a: os.path.join(os.path.dirname(__file__), "ui", "login.ui"))

Ui_MainWindow, _ = loadUiType(ui_path)

# 2. IMPORTANTE: Ahora heredamos de QMainWindow, no de QWidget
class LoginVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 3. Ocultamos la contraseña
        self.entradaContrasena.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Opcional: Permite iniciar sesión pulsando "Enter" desde la contraseña
        # self.entradaContrasena.returnPressed.connect(self.TU_BOTON_LOGIN.click)

    def obtener_credenciales(self) -> dict:
        """Extrae los datos para enviarlos al Controlador Principal"""
        return {
            "usuario": self.entradaUsuario.text().strip(),
            "password": self.entradaContrasena.text()
        }

    def limpiar_formulario(self):
        """Limpia las casillas"""
        self.entradaUsuario.clear()
        self.entradaContrasena.clear()
        self.entradaUsuario.setFocus()