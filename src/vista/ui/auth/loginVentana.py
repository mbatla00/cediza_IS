import os
from PySide6.QtWidgets import QMainWindow, QLineEdit, QMessageBox
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "login.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class LoginVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, auth_controller):
        super().__init__()
        self.setupUi(self)
        self._controller = auth_controller

        self.entradaContrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.entradaContrasena.returnPressed.connect(self.btn_login.click)
        self.btn_login.clicked.connect(self._on_login)

    def _on_login(self):
        usuario = self.entradaUsuario.text().strip()
        password = self.entradaContrasena.text()

        exito, mensaje, _ = self._controller.login(usuario, password)

        if exito:
            self._abrir_dashboard()
        else:
            QMessageBox.warning(self, "Error de acceso", mensaje)
            self.limpiar_formulario()

    def _abrir_dashboard(self):
        destino = self._controller.redirigir_segun_rol()
        datos = self._controller.get_usuario_actual_dict()

        if destino == 'admin_dashboard':
            from src.controlador.admin_controller import AdminController
            from src.vista.ui.admin.DashBoardAdminVentana import DashboardAdminVentana

            self._next = DashboardAdminVentana(AdminController(), self._controller, datos["nombreUsuario"])
            self._next.set_nombre_administrador(datos["nombre"])

        elif destino == 'trabajador_dashboard':
            from src.controlador.trabajador_controller import TrabajadorController
            from src.vista.ui.trabajador.trabajador_dashboardVentana import TrabajadorDashboardVentana

            self._next = TrabajadorDashboardVentana(TrabajadorController(datos["nombreUsuario"]))

        elif destino == 'paciente_dashboard':
            from src.controlador.paciente_controller import PacienteController
            from src.vista.ui.paciente.paciente_dashboardVentana import PacienteDashboardVentana

            self._next = PacienteDashboardVentana(PacienteController(datos["nombreUsuario"]))

        else:
            QMessageBox.critical(self, "Error", "Rol no reconocido")
            return

        self._next.show()
        self.close()

    def limpiar_formulario(self):
        self.entradaUsuario.clear()
        self.entradaContrasena.clear()
        self.entradaUsuario.setFocus()