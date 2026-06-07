import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "dashboardAdmin.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class DashboardAdminVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, admin_controller, auth_controller, usuario_actual):
        super().__init__()
        self.setupUi(self)
        self._controller = admin_controller
        self._auth_controller = auth_controller
        self._usuario_actual = usuario_actual
        self._conectar_botones()
        # Fuerza a la ventana a abrirse maximizada desde el inicio
        self.showMaximized()

    def _conectar_botones(self):
        self.btn_salir.clicked.connect(self._cerrar_sesion)
        self.btn_visualizar_perfil.clicked.connect(self._abrir_perfil)
        self.btn_nuevo_registro.clicked.connect(self._abrir_form_paciente)
        self.btn_nuevo_trabajador.clicked.connect(self._abrir_form_trabajador)
        self.btn_gestionar_usuarios.clicked.connect(self._abrir_usuarios)
        self.btn_crear_admin.clicked.connect(self._abrir_crear_admin)

    def set_nombre_administrador(self, nombre):
        self.lbl_bienvenida.setText(f"Bienvenid@, {nombre}")

    def _abrir_perfil(self):
        from src.vista.ui.admin.admin_perfilVentana import AdminPerfilVentana
        self._perfil = AdminPerfilVentana(self._controller, self._usuario_actual)
        self._perfil.show()

    def _abrir_form_paciente(self):
        from src.vista.ui.admin.paciente_formVentana import CrearPacienteVentana
        self._form_pac = CrearPacienteVentana(self._controller)
        self._form_pac.exec()

    def _abrir_form_trabajador(self):
        from src.vista.ui.admin.trabajador_formVentana import NuevoTrabajadorVentana
        self._form_trab = NuevoTrabajadorVentana(self._controller)
        self._form_trab.exec()

    def _abrir_usuarios(self):
        from src.vista.ui.admin.editar_usuarioVentana import AdminEditarUsuarioVentana
        self._usuarios = AdminEditarUsuarioVentana(self._controller)
        self._usuarios.show()

    def _abrir_crear_admin(self):
        from src.vista.ui.admin.crear_adminVentana import CrearAdminVentana
        self._crear_admin = CrearAdminVentana(self._controller)
        self._crear_admin.show()

    def _cerrar_sesion(self):
        self._auth_controller.logout()
        from src.vista.ui.auth.loginVentana import LoginVentana
        self._login = LoginVentana(self._auth_controller)
        self._login.show()
        self.close()