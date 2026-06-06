import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "dashboardAdmin.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class DashboardAdminVentana(QMainWindow, Ui_MainWindow):
    # AÑADIDO: Recibimos el usuario_actual (el username) en el constructor
    def __init__(self, admin_controller, usuario_actual):
        super().__init__()
        self.setupUi(self)
        self._controller = admin_controller
        self._usuario_actual = usuario_actual  # Lo guardamos para cuando abra el perfil
        self._conectar_botones()

    def _conectar_botones(self):
        self.btn_salir.clicked.connect(self._cerrar_sesion)
        self.btn_visualizar_perfil.clicked.connect(self._abrir_perfil)
        self.btn_nuevo_registro.clicked.connect(self._abrir_form_paciente)
        self.btn_nuevo_trabajador.clicked.connect(self._abrir_form_trabajador)
        self.btn_gestionar_usuarios.clicked.connect(self._abrir_usuarios)
        self.btn_crear_admin.clicked.connect(self._abrir_crear_admin)

    def set_nombre_administrador(self, nombre):
        self.lbl_bienvenida.setText(f"Bienvenido al centro de mando, {nombre}.")

    def _abrir_perfil(self):
        from src.vista.ui.admin.admin_perfilVentana import AdminPerfilVentana
        # Le pasamos el controlador Y el usuario actual
        self._perfil = AdminPerfilVentana(self._controller, self._usuario_actual)
        self._perfil.show()

    def _abrir_form_paciente(self):
        from src.vista.ui.admin.paciente_formVentana import CrearPacienteVentana
        self._form_pac = CrearPacienteVentana(self._controller)
        self._form_pac.exec()  # Usamos exec() para que sea una ventana modal

    def _abrir_form_trabajador(self):
        from src.vista.ui.admin.trabajador_formVentana import NuevoTrabajadorVentana
        self._form_trab = NuevoTrabajadorVentana(self._controller)
        self._form_trab.exec() # Usamos exec() para que sea una ventana modal

    def _abrir_usuarios(self):
        # Añadimos "Admin" al nombre de la clase para que coincida exactamente
        from src.vista.ui.admin.editar_usuarioVentana import AdminEditarUsuarioVentana
        self._usuarios = AdminEditarUsuarioVentana(self._controller)
        self._usuarios.show()

    def _abrir_crear_admin(self):
        from src.vista.ui.admin.crear_adminVentana import CrearAdminVentana
        self._crear_admin = CrearAdminVentana(self._controller)
        self._crear_admin.show()

    def _cerrar_sesion(self):
        from src.vista.ui.auth.loginVentana import LoginVentana
        from src.controlador.auth_controller import AuthController
        self._login = LoginVentana(AuthController())
        self._login.show()
        self.close()