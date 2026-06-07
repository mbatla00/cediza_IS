import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType

# Ruta al archivo .ui
ui_path = os.path.join(os.path.dirname(__file__), "cuestionario.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteCuestionarioVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        
        # 1. Configurar las opciones del ComboBox (Pregunta 2)
        # Usamos cmb_p2_horas (que es como seguramente se llama en tu UI)
        if hasattr(self, 'cmb_p2_horas'):
            self.cmb_p2_horas.clear()
            self.cmb_p2_horas.addItems([
                "Selecciona una opción",
                "Menos de 5 horas",
                "De 5 a 6 horas",
                "De 6 a 7 horas",
                "De 7 a 9 horas",
                "Más de 9 horas"
            ])
        elif hasattr(self, 'cmb_p2'):
            self.cmb_p2.clear()
            self.cmb_p2.addItems([
                "Selecciona una opción",
                "Menos de 5 horas",
                "De 5 a 6 horas",
                "De 6 a 7 horas",
                "De 7 a 9 horas",
                "Más de 9 horas"
            ])
        
        # 2. Estado inicial del campo condicional (Oculto)
        if hasattr(self, 'txt_p3_detalle'):
            self.txt_p3_detalle.setVisible(False)
        
        # 3. Conectar el RadioButton de la pregunta 3
        if hasattr(self, 'rad_p3_si'):
            self.rad_p3_si.toggled.connect(self.toggle_campo_que_hiciste)
        
        # 4. Conectar botones de acción
        if hasattr(self, 'btn_enviar'):
            self.btn_enviar.clicked.connect(self._validar_y_enviar)
        if hasattr(self, 'btn_cancelar'):
            self.btn_cancelar.clicked.connect(self.close)

    def toggle_campo_que_hiciste(self, checked: bool):
        """Muestra u oculta el campo de detalle según la selección."""
        if hasattr(self, 'txt_p3_detalle'):
            self.txt_p3_detalle.setVisible(checked)

    def _validar_y_enviar(self):
        # Determinar qué combobox existe en el UI
        combo_horas = self.cmb_p2_horas if hasattr(self, 'cmb_p2_horas') else self.cmb_p2

        if combo_horas.currentIndex() == 0:
            QMessageBox.warning(self, "Validación", "Por favor, selecciona las horas de sueño.")
            return

        if self.rad_p3_si.isChecked():
            if not self.txt_p3_detalle.toPlainText().strip():
                QMessageBox.warning(self, "Validación", "Por favor, detalla qué hiciste.")
                return

        if not self.txt_p4_desayuno.toPlainText().strip():
            QMessageBox.warning(self, "Validación", "Por favor, indica qué has desayunado.")
            return

        # ¡CORREGIDO! Generamos la lista estructurada INCLUYENDO EL ID DE CADA PREGUNTA
        # Se envían ambas claves 'contenido' y 'respuesta' por máxima compatibilidad con el backend
        respuestas = [
            {
                "idPregunta": 1, 
                "contenido": combo_horas.currentText(),
                "respuesta": combo_horas.currentText()
            },
            {
                "idPregunta": 2, 
                "contenido": "Sí" if self.rad_p3_si.isChecked() else "No",
                "respuesta": "Sí" if self.rad_p3_si.isChecked() else "No"
            },
            {
                "idPregunta": 3, 
                "contenido": self.txt_p3_detalle.toPlainText().strip() if self.rad_p3_si.isChecked() else "No aplica",
                "respuesta": self.txt_p3_detalle.toPlainText().strip() if self.rad_p3_si.isChecked() else "No aplica"
            },
            {
                "idPregunta": 4, 
                "contenido": self.txt_p4_desayuno.toPlainText().strip(),
                "respuesta": self.txt_p4_desayuno.toPlainText().strip()
            }
        ]
        
        exito, msg = self._controller.guardar_respuestas(respuestas)
        if exito:
            QMessageBox.information(self, "Éxito", "Cuestionario enviado correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)