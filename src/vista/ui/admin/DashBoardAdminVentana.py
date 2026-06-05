import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType

# Cargamos el archivo .ui de forma dinámica
ui_path = os.path.join(os.path.dirname(__file__), "dashboard_admin.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class DashboardAdminVentana(QMainWindow, Ui_MainWindow):
    # Señal para avisar a la ventana principal que queremos cambiar de vista
    cambiar_pantalla = Signal(str)

    def __init__(self, controlador=None):
        super().__init__()
        self.setupUi(self)
        
        self.controlador = controlador
        
        # Conectar los eventos de tus componentes
        self.conectar_eventos()

    def conectar_eventos(self):
        """ Vincula los botones del .ui con el sistema de navegación """
        self.btn_nuevo_registro.clicked.connect(lambda: self.gestionar_navegacion("pacientes"))
        self.btn_nuevo_trabajador.clicked.connect(lambda: self.gestionar_navegacion("trabajadores"))
        self.btn_gestionar_usuarios.clicked.connect(lambda: self.gestionar_navegacion("usuarios"))

    def set_nombre_administrador(self, nombre_admin: str):
        """ Cambia el texto del label_3 para mostrar el nombre del admin logueado """
        if nombre_admin:
            self.label_3.setText(f"Bienvenido al centro de mando, {nombre_admin}.")
        else:
            self.label_3.setText("Bienvenido al centro de mando.")

    def gestionar_navegacion(self, destino: str):
        """ Emite la señal con el destino para que tu QStackedWidget haga el cambio """
        print(f"[Dashboard Admin] Click detectado. Redirigiendo a: {destino}")
        self.cambiar_pantalla.emit(destino)