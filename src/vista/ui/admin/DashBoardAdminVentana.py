import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType

# Cargamos el archivo .ui de forma dinámica
ui_path = os.path.join(os.path.dirname(__file__), "dashboardAdmin.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class DashboardAdminVentana(QMainWindow, Ui_MainWindow):
    # Señal para notificar al controlador principal el cambio de pantalla o acción
    cambiar_pantalla = Signal(str)

    def __init__(self, controlador=None):
        super().__init__()
        self.setupUi(self)
        
        self.controlador = controlador
        
        # Conectar todos los eventos de los nuevos y antiguos componentes
        self.conectar_eventos()

    def conectar_eventos(self):
        """ Vincula los botones del .ui con el sistema de navegación """
        # Botones añadidos a la cabecera
        self.btn_salir.clicked.connect(lambda: self.gestionar_navegacion("salir"))
        self.btn_editar_perfil.clicked.connect(lambda: self.gestionar_navegacion("editar_perfil"))
        
        # Botones de las tarjetas principales
        self.btn_nuevo_registro.clicked.connect(lambda: self.gestionar_navegacion("pacientes"))
        self.btn_nuevo_trabajador.clicked.connect(lambda: self.gestionar_navegacion("trabajadores"))
        self.btn_gestionar_usuarios.clicked.connect(lambda: self.gestionar_navegacion("usuarios"))
        
        # Botón de la nueva tarjeta de administración
        self.btn_crear_admin.clicked.connect(lambda: self.gestionar_navegacion("crear_administrador"))

    def set_nombre_administrador(self, nombre_admin: str):
        """ Cambia el texto del label_3 de la cabecera para mostrar el admin activo """
        if nombre_admin:
            self.label_3.setText(f"Bienvenido al centro de mando, {nombre_admin}.")
        else:
            self.label_3.setText("Bienvenido al centro de mando.")

    def gestionar_navegacion(self, destino: str):
        """ Emite la señal correspondiente para que el controlador/main rutee la app """
        print(f"[Dashboard Admin] Click detectado -> Acción/Destino: {destino}")
        self.cambiar_pantalla.emit(destino)