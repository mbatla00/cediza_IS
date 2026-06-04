import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget
from PySide6.QtUiTools import loadUiType

# Cargar el archivo .ui del trabajador
ui_path = os.path.join(os.path.dirname(__file__), "ui", "trabajador_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Ajustes de comportamiento inicial
        self.configurar_interfaz()

    def configurar_interfaz(self):
        """Configuraciones estéticas de los componentes"""
        # Forzar a la tabla a expandirse de forma homogénea
        header = self.tabla_pacientes.horizontalHeader()
        header.setStretchLastSection(True)
        
        # Si usas modo de selección por filas completas (ideal para tu caso)
        self.tabla_pacientes.setSelectionBehavior(self.tabla_pacientes.SelectionBehavior.SelectRows)

    def inicializar_panel_segun_rol(self, tipo_trabajador: str):
        """
        Reemplaza el {% if tipo_trabajador == 'especialista' %} del HTML.
        Muestra u oculta la tarjeta de especialista según el usuario logueado.
        """
        es_especialista = (tipo_trabajador.lower() == "especialista")
        self.especialista.setVisible(es_especialista)
        
        # Si no es especialista, el QGridLayout redistribuirá el espacio automáticamente