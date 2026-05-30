import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

class DashboardAdminVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Construir la ruta relativa al archivo .ui
        # Asumiendo que DashboardAdmin.ui está en la carpeta 'ui' al lado de este archivo
        ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "DashboardAdmin.ui")
        
        #Cargar la interfaz del Administrador
        loadUi(ruta_ui, self)
        
        # Inicializaciones de cortesía (opcional)
        # Forzar a que la tabla se ajuste al ancho de la ventana
        self.usuarios_lista.horizontalHeader().setStretchLastSection(True)