import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

# Cargamos el archivo .ui de la evaluación
UI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
ui_path = os.path.join(UI_DIR, "evaluar_paciente.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class EvaluarPacienteVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def establecer_paciente_actual(self, nombre_paciente: str):
        """
        El controlador llama a este método al abrir la ventana para mostrar 
        a quién estamos evaluando.
        """
        self.lbl_paciente.setText(f"Evaluación Clínica para: {nombre_paciente}")

    def obtener_datos_evaluacion(self) -> dict:
        """
        Lee qué Radio Buttons están marcados y extrae la puntuación (1 al 5).
        Retorna un diccionario válido para el Modelo de Dominio, o None si faltan datos.
        """
        emocional = None
        movilidad = None
        apetito = None

        # 1. Comprobar Estado Emocional
        for i in range(1, 6):
            radio = getattr(self, f"rad_emocional_{i}")
            if radio.isChecked():
                emocional = i
                break

        # 2. Comprobar Movilidad
        for i in range(1, 6):
            radio = getattr(self, f"rad_movilidad_{i}")
            if radio.isChecked():
                movilidad = i
                break

        # 3. Comprobar Apetito
        for i in range(1, 6):
            radio = getattr(self, f"rad_apetito_{i}")
            if radio.isChecked():
                apetito = i
                break

        # Validación: Si falta alguno, avisamos al trabajador y cortamos el guardado
        if emocional is None or movilidad is None or apetito is None:
            QMessageBox.warning(
                self, 
                "Datos Incompletos", 
                "Por favor, puntúa todas las categorías obligatorias (Emocional, Movilidad y Apetito)."
            )
            return None

        # Si todo está bien, devolvemos el diccionario listo para la base de datos
        return {
            "estadoEmocional": emocional,
            "movilidad": movilidad,
            "apetito": apetito,
            "observaciones": self.txt_observaciones.toPlainText().strip()
        }

    def limpiar_formulario(self):
        """
        Desmarca todos los botones y limpia el texto para el siguiente paciente.
        """
        self.txt_observaciones.clear()
        
        # Desmarcamos de forma segura desactivando temporalmente la exclusividad
        for i in range(1, 6):
            for categoria in ["emocional", "movilidad", "apetito"]:
                radio = getattr(self, f"rad_{categoria}_{i}")
                radio.setAutoExclusive(False)
                radio.setChecked(False)
                radio.setAutoExclusive(True)