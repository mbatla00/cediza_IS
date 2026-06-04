import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType

# 1. Localizar y cargar el archivo .ui de forma dinámica
ui_path = os.path.join(os.path.dirname(__file__), "ui", "DashboardAdmin.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class DashboardAdminVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        # 2. Construir la interfaz reflejando el XML
        self.setupUi(self)
        
        # 3. Ajustes de comportamiento estético para tus componentes
        self.configurar_interfaz()
        
        # 4. Enlaces de navegación interna (Comportamiento visual puro)
        self.btn_perfil_volver.clicked.connect(self.volver_a_pestaña_inicio)

    def configurar_interfaz(self):
        """Configuraciones iniciales de la vista al arrancar"""
        # Forzar a que la última columna de la tabla ('acción') ocupe el espacio restante
        self.usuarios_lista.horizontalHeader().setStretchLastSection(True)
        
        # Opcional: Ocultar la contraseña por defecto en el campo de texto de perfil
        self.txt_perfil_password.setEchoMode(self.txt_perfil_password.EchoMode.Password)

    def volver_a_pestaña_inicio(self):
        """Redirige al usuario a la primera pestaña de tu QTabWidget (Crear Perfiles)"""
        # Como en tu XML el QTabWidget se llama 'dashboard', accedemos a él directamente
        self.dashboard.setCurrentIndex(0)