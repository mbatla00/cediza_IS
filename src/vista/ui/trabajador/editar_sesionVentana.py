import os
from datetime import datetime, date, time
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate, QTime

ui_path = os.path.join(os.path.dirname(__file__), "editar_sesion.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorEditarSesionVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador, sesion_id):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self._sesion_id = sesion_id

        self.txt_paciente.setReadOnly(True)
        self.btn_cancelar.clicked.connect(self.close)
        self.btn_guardar.clicked.connect(self._procesar_guardado)

    def cargar_datos_sesion(self, sesion: dict):
        self.txt_paciente.setText(sesion.get("paciente", ""))
        self.txt_comentarios.setPlainText(sesion.get("comentarios", ""))

        fecha_val = sesion.get("fecha")
        if isinstance(fecha_val, (date, datetime)):
            self.date_sesion.setDate(QDate(fecha_val.year, fecha_val.month, fecha_val.day))
        elif isinstance(fecha_val, str) and fecha_val:
            f = datetime.strptime(fecha_val, "%Y-%m-%d").date()
            self.date_sesion.setDate(QDate(f.year, f.month, f.day))

        hora_val = sesion.get("hora")
        if isinstance(hora_val, time):
            self.time_sesion.setTime(QTime(hora_val.hour, hora_val.minute))
        elif isinstance(hora_val, str) and hora_val:
            h = datetime.strptime(hora_val[:5], "%H:%M").time()
            self.time_sesion.setTime(QTime(h.hour, h.minute))

    def _procesar_guardado(self):
        datos = {
            "fecha": self.date_sesion.date().toString("yyyy-MM-dd"),
            "hora": self.time_sesion.time().toString("HH:mm"),
            "comentarios": self.txt_comentarios.toPlainText().strip()
        }
        exito, msg = self._controller.actualizar_sesion(self._sesion_id, datos)
        if exito:
            QMessageBox.information(self, "Éxito", "Sesión actualizada correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)