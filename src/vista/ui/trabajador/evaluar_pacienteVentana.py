import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "evaluar_paciente.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class EvaluarPacienteVentana(QMainWindow, Ui_MainWindow):
    """
    Ventana del formulario de evaluación clínica periódica del paciente.
    Permite al profesional puntuar el estado emocional, movilidad y apetito,
    además de añadir observaciones adicionales en texto libre.
    """
    def __init__(self, controlador, nombre_paciente):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self._nombre_paciente = nombre_paciente

        self.lbl_paciente.setText(f"Evaluación Clínica para: {nombre_paciente}")
        self.btn_volver.clicked.connect(self.close)
        self.btn_guardar.clicked.connect(self._procesar_guardado)
        self.showMaximized()

    def _obtener_datos_evaluacion(self):
        emocional = movilidad = apetito = None
        for i in range(1, 6):
            if getattr(self, f"rad_emocional_{i}").isChecked(): emocional = i
            if getattr(self, f"rad_movilidad_{i}").isChecked(): movilidad = i
            if getattr(self, f"rad_apetito_{i}").isChecked(): apetito = i
        
        # VALIDACIÓN: Garantiza que el profesional haya puntuado obligatoriamente las 3 categorías
        if None in (emocional, movilidad, apetito):
            QMessageBox.warning(self, "Datos Incompletos", "Puntúa todas las categorías.")
            return None

        return {
            "paciente": self._nombre_paciente,
            "estadoEmocional": emocional,
            "movilidad": movilidad,
            "apetito": apetito,
            "observaciones": self.txt_observaciones.toPlainText().strip()
        }

    def _procesar_guardado(self):
        # Extrae los datos previamente validados
        datos = self._obtener_datos_evaluacion()
        if datos is None:
            return
        exito, msg = self._controller.guardar_evaluacion(datos)
        # Respuesta visual al usuario según el resultado del backend
        if exito:
            QMessageBox.information(self, "Éxito", "Evaluación guardada correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)