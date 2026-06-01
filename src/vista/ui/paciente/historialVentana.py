import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

# Cargar el archivo .ui del historial
ui_path = os.path.join(os.path.dirname(__file__), "ui", "historial.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteHistorialVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def cargar_historial(self, historial_agrupado: dict, preguntas_dict: dict):
        """
        Replica el motor de plantillas de Jinja2 en PySide6.
        Muestra las respuestas agrupadas por fecha en orden descendente.
        """
        # Limpiar el contenedor por si la vista se vuelve a abrir/actualizar
        self.limpiar_layout_historial()
        
        # Obtener el layout vertical que está DENTRO del QScrollArea
        layout_principal = self.scrollAreaWidgetContents.layout()
        
        # Caso {% else %}: Si el historial está vacío
        if not historial_agrupado:
            lbl_vacio = QLabel("ℹTodavía no has respondido ningún cuestionario.")
            lbl_vacio.setStyleSheet("color: #6c757d; font-style: italic; font-size: 13px; padding: 20px;")
            lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_principal.addWidget(lbl_vacio)
            return

        # Ordenar las fechas de forma descendente (igual que el | sort(reverse=True) del HTML)
        fechas_ordenadas = sorted(historial_agrupado.keys(), reverse=True)
        
        for fecha in fechas_ordenadas:
            respuestas = historial_agrupado[fecha]
            
            # 1. Crear el bloque para el día (Un QWidget contenedor)
            bloque_dia = QWidget()
            layout_dia = QVBoxLayout(bloque_dia)
            layout_dia.setContentsMargins(0, 0, 0, 15) # Margen abajo para separar los días
            
            # 2. Convertir la fecha a texto (Formato dd/mm/yyyy)
            fecha_str = fecha.strftime('%d/%m/%Y') if fecha else "Sin fecha"
            
            # 3. Componente de Título de la Fecha
            lbl_fecha = QLabel(f"{fecha_str}")
            # Le aplicamos CSS para simular el 'text-secondary border-bottom' de Bootstrap
            lbl_fecha.setStyleSheet("""
                font-size: 14px; 
                font-weight: bold; 
                color: #495057; 
                border-bottom: 1px solid #dee2e6; 
                padding-bottom: 5px;
            """)
            layout_dia.addWidget(lbl_fecha)
            
            # 4. Segundo bucle: Recorrer las respuestas de esa fecha concreta
            for respuesta in respuestas:
                # Buscar el texto de la pregunta usando el ID
                texto_pregunta = preguntas_dict.get(respuesta.idPregunta, "Pregunta no disponible")
                texto_respuesta = respuesta.contenido
                
                # Crear un sub-contenedor para el par Pregunta/Respuesta (para darle un margen izquierdo 'ps-2')
                contenedor_item = QWidget()
                layout_item = QVBoxLayout(contenedor_item)
                layout_item.setContentsMargins(15, 5, 0, 5) # 15px de margen izquierdo
                layout_item.setSpacing(2) # Espacio muy corto entre pregunta y respuesta
                
                # Label de la Pregunta (fw-bold text-dark)
                lbl_pregunta = QLabel(texto_pregunta)
                lbl_pregunta.setWordWrap(True) # ¡Importante para que no se corte el texto!
                lbl_pregunta.setStyleSheet("font-weight: bold; color: #212529; font-size: 13px;")
                
                # Label del Contenido de la respuesta (text-muted)
                lbl_respuesta = QLabel(f"{texto_respuesta}")
                lbl_respuesta.setWordWrap(True)
                lbl_respuesta.setStyleSheet("color: #6c757d; font-size: 13px;")
                
                # Añadir los textos al contenedor del ítem
                layout_item.addWidget(lbl_pregunta)
                layout_item.addWidget(lbl_respuesta)
                
                # Añadir el ítem al layout del día
                layout_dia.addWidget(contenedor_item)
            
            # Finalmente, añadir el bloque del día completo al Scroll Area
            layout_principal.addWidget(bloque_dia)

    def limpiar_layout_historial(self):
        """Elimina todos los widgets dinámicos creados anteriormente"""
        layout = self.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()