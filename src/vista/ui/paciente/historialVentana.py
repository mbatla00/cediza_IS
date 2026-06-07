import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

ui_path = os.path.join(os.path.dirname(__file__), "historial.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteHistorialVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self.btn_volver.clicked.connect(self.close)
        self._cargar_datos()

    def _cargar_datos(self):
        historial = self._controller.obtener_historial_agrupado_por_fecha()
        preguntas = self._controller.obtener_preguntas_dict()
        self._mostrar_historial(historial, preguntas)

    def _mostrar_historial(self, historial_agrupado: dict, preguntas_dict: dict):
        self._limpiar_layout_historial()

        layout_principal = self.scrollAreaWidgetContents.layout()

        if not historial_agrupado:
            lbl_vacio = QLabel("ℹ Todavía no has respondido ningún cuestionario.")
            lbl_vacio.setStyleSheet("color: #6c757d; font-style: italic; font-size: 13px; padding: 20px;")
            lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_principal.addWidget(lbl_vacio)
            return

        fechas_ordenadas = sorted(historial_agrupado.keys(), reverse=True)

        for fecha in fechas_ordenadas:
            respuestas = historial_agrupado[fecha]

            bloque_dia = QWidget()
            layout_dia = QVBoxLayout(bloque_dia)
            layout_dia.setContentsMargins(0, 0, 0, 15)

            fecha_str = fecha.strftime('%d/%m/%Y') if fecha else "Sin fecha"

            lbl_fecha = QLabel(fecha_str)
            lbl_fecha.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                border-bottom: 1px solid #dee2e6;
                padding-bottom: 5px;
            """)
            layout_dia.addWidget(lbl_fecha)

            for respuesta in respuestas:
                # Corregido: 'respuesta' ahora es tratada como un diccionario básico
                id_preg = respuesta.get('idPregunta')
                texto_pregunta = preguntas_dict.get(id_preg, "Pregunta no disponible")
                texto_respuesta = respuesta.get('contenido', '')

                contenedor_item = QWidget()
                layout_item = QVBoxLayout(contenedor_item)
                layout_item.setContentsMargins(15, 5, 0, 5)
                layout_item.setSpacing(2)

                lbl_pregunta = QLabel(texto_pregunta)
                lbl_pregunta.setWordWrap(True)
                lbl_pregunta.setStyleSheet("font-weight: bold; color: #212529; font-size: 13px;")

                lbl_respuesta = QLabel(str(texto_respuesta))
                lbl_respuesta.setWordWrap(True)
                lbl_respuesta.setStyleSheet("color: #6c757d; font-size: 13px;")

                layout_item.addWidget(lbl_pregunta)
                layout_item.addWidget(lbl_respuesta)

                layout_dia.addWidget(contenedor_item)

            layout_principal.addWidget(bloque_dia)

    def _limpiar_layout_historial(self):
        layout = self.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()