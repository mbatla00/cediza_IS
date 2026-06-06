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
        
        # Aquí obtenemos el usuario_vo de la base de datos
        exito, mensaje, usuario_vo = self._controller.login(usuario, password)

        if exito:
            # Le pasamos el usuario_vo a la función que abre el dashboard
            self._abrir_dashboard(usuario_vo)
        else:
            QMessageBox.warning(self, "Error de acceso", mensaje)
            self.limpiar_formulario()

    def _abrir_dashboard(self, usuario_vo):
        # CORREGIDO: Llamada al método sin parámetros
        destino = self._controller.redirigir_segun_rol()
        
        if destino == 'admin_dashboard':
            from src.controlador.admin_controller import AdminController
            from src.vista.ui.admin.DashBoardAdminVentana import DashboardAdminVentana
            
            # Pasamos el controlador y el username (nombreUsuario) al constructor
            self._next = DashboardAdminVentana(AdminController(), usuario_vo.nombreUsuario)
            
            # Usamos el nombre real para configurar el cartel de "Bienvenido, Alejandro"
            self._next.set_nombre_administrador(getattr(usuario_vo, 'nombre', usuario_vo.nombreUsuario))

        elif destino == 'trabajador_dashboard':
            from src.controlador.trabajador_controller import TrabajadorController
            from src.vista.ui.trabajador.trabajador_dashboardVentana import TrabajadorDashboardVentana
            
            # Se le pasa el usuario al TrabajadorController
            self._next = TrabajadorDashboardVentana(TrabajadorController(usuario_vo.nombreUsuario))

        elif destino == 'paciente_dashboard':
            from src.controlador.paciente_controller import PacienteController
            from src.vista.ui.paciente.paciente_dashboardVentana import PacienteDashboardVentana
            self._next = PacienteDashboardVentana(PacienteController())

        else:
            QMessageBox.critical(self, "Error", "Rol no reconocido")
            return

        self._next.show()
        self.close()

    def limpiar_formulario(self):
        self.entradaUsuario.clear()
        self.entradaContrasena.clear()
        self.entradaUsuario.setFocus()