import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "ui", "cuestionario.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteCuestionarioVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 1. Configurar las opciones fijas del ComboBox (Pregunta 2)
        self.cmb_p2_horas.clear()
        self.cmb_p2_horas.addItems([
            "Selecciona una opción",
            "Menos de 5 horas",
            "De 5 a 6 horas",
            "De 6 a 7 horas",
            "De 7 a 9 horas",
            "Más de 9 horas"
        ])
        
        # 2. Estado inicial del campo condicional (Oculto por defecto)
        self.widget_p3_detalle.setVisible(False)
        
        # 3. Conectar el evento del Radio Button 
        # El evento 'toggled' se dispara tanto al marcar como al desmarcar
        self.rad_p3_si.toggled.connect(self.toggle_campo_que_hiciste)

    def toggle_campo_que_hiciste(self, checked: bool):
        """
        Replica exactamente la función de JavaScript.
        Muestra u oculta el campo de texto según la elección del paciente.
        """
        # Si 'checked' es True, significa que el usuario ha marcado el "Sí"
        self.widget_p3_detalle.setVisible(checked)
        if not checked:
            self.txt_p3_detalle.clear() # Limpiar el texto si cambia a "No"

    def validar_y_obtener_respuestas(self) -> dict | None:
        """
        Verifica que el usuario haya respondido todo lo obligatorio (required)
        y extrae las respuestas simulando el envío del formulario.
        """
        # Validar Pregunta 1 (Radio Buttons)
        estado_hoy = ""
        if self.rad_p1_bien.isChecked(): estado_hoy = "Bien"
        elif self.rad_p1_regular.isChecked(): estado_hoy = "Regular"
        elif self.rad_p1_mal.isChecked(): estado_hoy = "Mal"
        
        if not estado_hoy:
            QMessageBox.warning(self, "Validación", "Por favor, responde cómo te encuentras hoy.")
            return None

        # Validar Pregunta 2 (ComboBox)
        if self.cmb_p2_horas.currentIndex() == 0: # "Selecciona una opción"
            QMessageBox.warning(self, "Validación", "Por favor, selecciona las horas de sueño.")
            return None
        horas_sueno = self.cmb_p2_horas.currentText()

        # Validar Pregunta 3 (Condicional)
        recuerda_ayer = ""
        que_hizo_ayer = "-"
        if self.rad_p3_si.isChecked():
            recuerda_ayer = "Si"
            que_hizo_ayer = self.txt_p3_detalle.toPlainText().strip()
            if not que_hizo_ayer:
                QMessageBox.warning(self, "Validación", "Por favor, detalla qué hiciste ayer por la tarde.")
                return None
        elif self.rad_p3_no.isChecked():
            recuerda_ayer = "No"
        else:
            QMessageBox.warning(self, "Validación", "Por favor, responde si recuerdas qué hiciste ayer.")
            return None

        # Validar Pregunta 4 (Text Area)
        desayuno = self.txt_p4_desayuno.toPlainText().strip()
        if not desayuno:
            QMessageBox.warning(self, "Validación", "Por favor, responde qué has desayunado hoy.")
            return None

        # Si todo está correcto, devolvemos el diccionario estructurado
        return {
            "respuesta_1": estado_hoy,
            "respuesta_2": horas_sueno,
            "respuesta_3_si_no": recuerda_ayer,
            "respuesta_3": que_hizo_ayer,
            "respuesta_4": desayuno
        }