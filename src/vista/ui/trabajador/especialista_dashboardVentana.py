import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate, QTime

ui_path = os.path.join(os.path.dirname(__file__), "especialista_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class EspecialistaDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador

        self.date_fecha.setDate(QDate.currentDate())
        self.time_hora.setTime(QTime.currentTime())
        self._configurar_tablas()
        self._conectar_botones()
        self._cargar_datos()

    def _configurar_tablas(self):
        columnas = ["Fecha", "Hora", "Paciente", "Comentarios", "Acciones"]
        for tabla in [self.tabla_proximas, self.tabla_pasadas]:
            tabla.setColumnCount(len(columnas))
            tabla.setHorizontalHeaderLabels(columnas)
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tabla.verticalHeader().setVisible(False)
            
            # LÍNEAS CORREGIDAS: Uso seguro de QAbstractItemView
            from PySide6.QtWidgets import QAbstractItemView
            tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def _conectar_botones(self):
        self.btn_crear_sesion.clicked.connect(self._procesar_nueva_sesion)
        self.btn_volver.clicked.connect(self.close)

    def _cargar_datos(self):
        pacientes = self._controller.listar_pacientes()
        self.cmb_paciente.clear()
        self.cmb_paciente.addItem("-- Seleccionar paciente --", None)
        for p in pacientes:
            self.cmb_paciente.addItem(getattr(p, 'nombre', ''), getattr(p, 'nombreUsuario', ''))

        sesiones = self._controller.listar_sesiones_como_especialista()
        self.tabla_proximas.setRowCount(0)
        self.tabla_pasadas.setRowCount(0)
        from datetime import date
        hoy = date.today()
        for s in (sesiones or []):
            fecha = getattr(s, 'fecha', None)
            tabla = self.tabla_proximas if fecha and fecha >= hoy else self.tabla_pasadas
            self._agregar_sesion_a_tabla(tabla, s)

    def _agregar_sesion_a_tabla(self, tabla, sesion):
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        tabla.setItem(fila, 0, QTableWidgetItem(str(getattr(sesion, 'fecha', ''))))
        tabla.setItem(fila, 1, QTableWidgetItem(str(getattr(sesion, 'hora', ''))))
        tabla.setItem(fila, 2, QTableWidgetItem(str(getattr(sesion, 'paciente', ''))))
        tabla.setItem(fila, 3, QTableWidgetItem(str(getattr(sesion, 'comentarios', ''))))

        btn_editar = QPushButton("✏️ Editar")
        btn_editar.setProperty("sesion_id", getattr(sesion, 'idSesion', None))
        btn_editar.setProperty("sesion_data", {
            "paciente": getattr(sesion, 'paciente', ''),
            "fecha": str(getattr(sesion, 'fecha', '')),
            "hora": str(getattr(sesion, 'hora', '')),
            "comentarios": getattr(sesion, 'comentarios', '')
        })
        btn_editar.clicked.connect(self._abrir_editar_sesion)
        tabla.setCellWidget(fila, 4, btn_editar)
        tabla.setRowHeight(fila, 40)

    def _abrir_editar_sesion(self):
        boton = self.sender()
        sesion_id = boton.property("sesion_id")
        sesion_data = boton.property("sesion_data")
        from src.vista.ui.trabajador.editar_sesionVentana import TrabajadorEditarSesionVentana
        self._editar = TrabajadorEditarSesionVentana(self._controller, sesion_id)
        self._editar.cargar_datos_sesion(sesion_data)
        self._editar.show()

    def _procesar_nueva_sesion(self):
        paciente_usuario = self.cmb_paciente.currentData()
        if not paciente_usuario:
            QMessageBox.warning(self, "Error", "Debe seleccionar un paciente.")
            return
        datos = {
            "paciente": paciente_usuario,
            "fecha": self.date_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.time_hora.time().toString("HH:mm"),
            "comentarios": self.txt_comentarios.toPlainText().strip()
        }
        exito, msg = self._controller.crear_sesion(datos)
        if exito:
            QMessageBox.information(self, "Éxito", "Sesión programada correctamente.")
            self.cmb_paciente.setCurrentIndex(0)
            self.txt_comentarios.clear()
            self._cargar_datos()
        else:
            QMessageBox.warning(self, "Error", msg)