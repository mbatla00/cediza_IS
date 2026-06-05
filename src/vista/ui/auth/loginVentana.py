import os
from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtUiTools import loadUiType

# Cargamos de forma dinámica el archivo .ui que está en esta misma carpeta
ui_path = os.path.join(os.path.dirname(__file__), "login.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class LoginVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Asegura que la contraseña se oculte con asteriscos/puntos en la interfaz
        self.entradaContrasena.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Si el usuario pulsa 'Enter' al escribir la contraseña, se simula el clic en el botón azul
        self.entradaContrasena.returnPressed.connect(self.btn_login.click)

    def obtener_credenciales(self) -> dict:
        """
        Devuelve un diccionario con los datos introducidos.
        El controlador usará este método para validar el acceso.
        """
        return {
            "usuario": self.entradaUsuario.text().strip(),
            "password": self.entradaContrasena.text()
        }

    def limpiar_formulario(self):
        """
        Limpia las cajas de texto y pone el foco en el usuario.
        Útil si hay un error de login o si se cierra sesión.
        """
        self.entradaUsuario.clear()
        self.entradaContrasena.clear()
        self.entradaUsuario.setFocus()