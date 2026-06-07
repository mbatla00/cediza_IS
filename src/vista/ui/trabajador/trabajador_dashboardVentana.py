import os
from PySide6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QAbstractItemView, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

ui_path = os.path.join(os.path.dirname(__file__), "trabajador_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self._configurar_tabla()
        self._conectar_botones()
        self._cargar_datos()

    def _configurar_tabla(self):
        header = self.tabla_pacientes.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabla_pacientes.verticalHeader().setVisible(False)
        self.tabla_pacientes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_pacientes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_pacientes.doubleClicked.connect(self._abrir_detalle_paciente)

    def _conectar_botones(self):
        self.btn_salir.clicked.connect(self._cerrar_sesion)
        self.btn_perfil.clicked.connect(self._abrir_perfil)
        self.btn_evaluar.clicked.connect(self._abrir_evaluacion)
        self.btn_anadir_nota.clicked.connect(self._abrir_nota)

        # Se normaliza a minúsculas para evitar fallos de mayúsculas/minúsculas desde la BD
        tipo = self._controller.obtener_tipo_trabajador()
        self.especialista.setVisible(tipo.lower() == 'especialista' if tipo else False)
        if tipo and tipo.lower() == 'especialista':
            self.btn_especialista.clicked.connect(self._abrir_dashboard_especialista)

    def _cargar_datos(self):
        # AHORA utilizamos el método dict del controlador
        pacientes = self._controller.listar_pacientes_dict()
        self.tabla_pacientes.setRowCount(0)
        self.cmb_evaluar_paciente.clear()
        self.cmb_nota_paciente.clear()

        for i, p in enumerate(pacientes or []):
            self.tabla_pacientes.insertRow(i)

            # Reemplazamos getattr por el método seguro .get() de los diccionarios
            datos = [
                p.get('nombreUsuario', ''),
                p.get('nombre', ''),
                p.get('tipo', ''),
                p.get('dni', ''),
            ]
            for col, valor in enumerate(datos):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_pacientes.setItem(i, col, item)

            # Rellenamos los ComboBoxes de las tarjetas superiores
            nombre = p.get('nombre', '')
            usuario = p.get('nombreUsuario', '')
            self.cmb_evaluar_paciente.addItem(nombre, usuario)
            self.cmb_nota_paciente.addItem(nombre, usuario)

    def _abrir_evaluacion(self):
        paciente_usuario = self.cmb_evaluar_paciente.currentData()
        if not paciente_usuario:
            QMessageBox.warning(self, "Aviso", "Selecciona un paciente.")
            return
        from src.vista.ui.trabajador.evaluar_pacienteVentana import EvaluarPacienteVentana
        self._eval = EvaluarPacienteVentana(self._controller, paciente_usuario)
        self._eval.show()

    def _abrir_nota(self):
        paciente_usuario = self.cmb_nota_paciente.currentData()
        if not paciente_usuario:
            QMessageBox.warning(self, "Aviso", "Selecciona un paciente.")
            return
        from src.vista.ui.trabajador.paciente_detalleVentana import PacienteDetalleVentana
        self._detalle = PacienteDetalleVentana(self._controller, paciente_usuario)
        self._detalle.show()

    def _abrir_detalle_paciente(self, index):
        nombre_usuario = self.tabla_pacientes.item(index.row(), 0).text()
        from src.vista.ui.trabajador.paciente_detalleVentana import PacienteDetalleVentana
        self._detalle = PacienteDetalleVentana(self._controller, nombre_usuario)
        self._detalle.show()

    def _abrir_perfil(self):
        from src.vista.ui.trabajador.trabajador_perfilVentana import TrabajadorPerfilVentana
        self._perfil = TrabajadorPerfilVentana(self._controller)
        self._perfil.show()

    def _abrir_dashboard_especialista(self):
        from src.vista.ui.trabajador.especialista_dashboardVentana import EspecialistaDashboardVentana
        self._esp = EspecialistaDashboardVentana(self._controller)
        self._esp.show()

    def _cerrar_sesion(self):
        from src.vista.ui.auth.loginVentana import LoginVentana
        from src.controlador.auth_controller import AuthController
        self._login = LoginVentana(AuthController())
        self._login.show()
        self.hide()