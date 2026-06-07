import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "paciente_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self._cargar_datos()
        self._conectar_botones()
        self.showMaximized()

    def _conectar_botones(self):
        self.btn_cuestionario_diario.clicked.connect(self._abrir_cuestionario)
        self.btn_ver_historial.clicked.connect(self._abrir_historial)
        self.btn_informacion_personal.clicked.connect(self._abrir_perfil)
        self.btn_sesiones.clicked.connect(self._abrir_sesiones)
        self.btn_volver.clicked.connect(self._cerrar_sesion)

    def _cargar_datos(self):
        datos = self._controller.obtener_perfil_dict()
        if datos:
            nombre = datos.get("nombre") or datos.get("nombreUsuario", "")
            self.label_3.setText(f"¡Hola, {nombre}! ¿Qué te gustaría hacer hoy?")

        ya_respondio = self._controller.ya_respondio_hoy()
        if ya_respondio:
            self.label_7.setText("¡Ya has completado el cuestionario de hoy!")
            self.label_7.setStyleSheet("color: #198754; font-weight: bold;")
            self.btn_cuestionario_diario.setText("Completado por hoy")
            self.btn_cuestionario_diario.setEnabled(False)
        else:
            self.label_7.setText("Ayúdanos a saber cómo te encuentras hoy.")
            self.label_7.setStyleSheet("color: #6c757d; font-weight: bold;")
            self.btn_cuestionario_diario.setText("Empezar cuestionario")
            self.btn_cuestionario_diario.setEnabled(True)

    def _abrir_cuestionario(self):
        from src.vista.ui.paciente.cuestionarioVentana import PacienteCuestionarioVentana
        self._cuestionario = PacienteCuestionarioVentana(self._controller)
        self._cuestionario.show()

    def _abrir_historial(self):
        from src.vista.ui.paciente.historialVentana import PacienteHistorialVentana
        self._historial = PacienteHistorialVentana(self._controller)
        self._historial.show()

    def _abrir_perfil(self):
        from src.vista.ui.paciente.paciente_perfilVentana import PacientePerfilVentana
        self._perfil = PacientePerfilVentana(self._controller)
        self._perfil.show()

    def _abrir_sesiones(self):
        from src.vista.ui.paciente.sesionesVentana import PacienteSesionesVentana
        self._sesiones = PacienteSesionesVentana(self._controller)
        self._sesiones.show()

    def _cerrar_sesion(self):
        from src.vista.ui.auth.loginVentana import LoginVentana
        from src.controlador.auth_controller import AuthController
        self._login_window = LoginVentana(AuthController())
        self._login_window.show()
        self.close()