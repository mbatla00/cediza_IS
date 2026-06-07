import os
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

ui_path = os.path.join(os.path.dirname(__file__), "paciente_perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacientePerfilVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self.btn_volver.clicked.connect(self.close)
        self._configurar_tabla()
        self._cargar_datos()
        self.showMaximized()

    def _configurar_tabla(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setVisible(True)
        header.setMinimumHeight(35)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setMinimumHeight(180)
        self.tableWidget.setContentsMargins(0, 0, 0, 0)

    def _cargar_datos(self):
        datos = self._controller.obtener_perfil_dict()
        if not datos:
            return

        # Datos de cuenta
        self.txt_usuario.setText(datos.get("nombreUsuario", ""))
        self.txt_email.setText(datos.get("email", "Sin correo registrado"))
        self.txt_telefono.setText(str(datos.get("telefono", "No registrado")))

        # Datos personales
        self.txt_nombre.setText(datos.get("nombre", ""))
        self.txt_dni.setText(datos.get("dni", ""))
        fecha = datos.get("fechaNacimiento", "No registrada")
        self.txt_fecha_naciemiento.setText(str(fecha) if fecha else "No registrada")

        # Familiares en la tabla (Corregido para usar diccionarios y .get)
        familiares = self._controller.listar_familiares_dict()
        self.tableWidget.setRowCount(0)
        for i, f in enumerate(familiares or []):
            self.tableWidget.insertRow(i)
            campos = [
                f.get('nombre', ''),
                f.get('relacion', f.get('Relacion', '')),
                f.get('telefono', f.get('Telefono', ''))
            ]
            for col, valor in enumerate(campos):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(i, col, item)