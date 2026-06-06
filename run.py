import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.controlador.auth_controller import AuthController
from src.vista.ui.auth.loginVentana import LoginVentana

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    auth_controller = AuthController()
    ventana_login = LoginVentana(auth_controller)  # le pasamos el controlador
    ventana_login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()