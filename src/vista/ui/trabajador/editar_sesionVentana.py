import os
from datetime import datetime, date, time
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate, QTime

# Cargar el archivo .ui exclusivo de edición de sesión
ui_path = os.path.join(os.path.dirname(__file__), "ui", "editar_sesion.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorEditarSesionVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def cargar_datos_sesion(self, sesion: dict):
        """
        Rellena el formulario con los datos de la sesión seleccionada.
        Soporta strings y objetos nativos de Python.
        """
        self.txt_paciente.setText(sesion.get("paciente", "Paciente No Especificado"))
        self.txt_comentarios.setPlainText(sesion.get("comentarios", ""))

        # 1. Procesar y setear la Fecha
        fecha_val = sesion.get("fecha")
        if isinstance(fecha_val, (date, datetime)):
            self.date_sesion.setDate(QDate(fecha_val.year, fecha_val.month, fecha_val.day))
        elif isinstance(fecha_val, str) and fecha_val:
            # Por si te llega de la BD como "YYYY-MM-DD"
            f = datetime.strptime(fecha_val, "%Y-%m-%d").date()
            self.date_sesion.setDate(QDate(f.year, f.month, f.day))
        else:
            self.date_sesion.setDate(QDate.currentDate())

        # 2. Procesar y setear la Hora
        hora_val = sesion.get("hora")
        if isinstance(hora_val, time):
            self.time_sesion.setTime(QTime(hora_val.hour, hora_val.minute))
        elif isinstance(hora_val, str) and hora_val:
            # Por si te llega de la BD como "HH:MM"
            h = datetime.strptime(hora_val, "%H:%M").time()
            self.time_sesion.setTime(QTime(h.hour, h.minute))
        else:
            self.time_sesion.setTime(QTime(12, 0)) # Hora por defecto uniforme

    def obtener_datos_formulario(self) -> dict:
        """
        Extrae la información modificada por el especialista para pasarla al controlador.
        Devuelve cadenas formateadas listas para tu backend.
        """
        qdate = self.date_sesion.date()
        qtime = self.time_sesion.time()

        # Formateo idéntico a las necesidades de un backend SQL/ORM standard
        fecha_str = f"{qdate.year()}-{qdate.month():02d}-{qdate.day():02d}"
        hora_str = f"{qtime.hour():02d}:{qtime.minute():02d}"

        return {
            "fecha": fecha_str,
            "hora": hora_str,
            "comentarios": self.txt_comentarios.toPlainText().strip()
        }