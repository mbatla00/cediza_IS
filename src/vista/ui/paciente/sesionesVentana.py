import os
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import loadUiType

# Cargar el archivo .ui de las sesiones
ui_path = os.path.join(os.path.dirname(__file__), "ui", "sesiones.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteSesionesVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Ajustar automáticamente el ancho de las columnas al abrir
        self.tabla_proximas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_pasadas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def cargar_sesiones(self, proximas: list, pasadas: list):
        """
        Rellena las tablas de sesiones próximas y pasadas.
        Replica la lógica condicional del HTML.
        """
        self._rellenar_tabla(self.tabla_proximas, proximas, "No tienes sesiones próximas programadas.")
        self._rellenar_tabla(self.tabla_pasadas, pasadas, "No tienes sesiones pasadas.")

    def _rellenar_tabla(self, tabla, lista_sesiones, mensaje_vacio):
        """Método interno auxiliar para evitar duplicar código de renderizado"""
        tabla.setRowCount(0) # Limpiar datos anteriores
        
        # Caso {% else %}: Si la lista viene vacía
        if not lista_sesiones:
            tabla.setRowCount(1)
            # Combinamos las 4 columnas para poner el mensaje de error centrado (colspan="4")
            tabla.setSpan(0, 0, 1, 4) 
            item = QTableWidgetItem(mensaje_vacio)
            item.setTextAlignment(0x0004 | 0x0080) # Centrado horizontal y vertical
            tabla.setItem(0, 0, item)
            return

        # Caso {% for s in ... %}: Rellenar con los objetos de la base de datos
        for fila, s in enumerate(lista_sesiones):
            tabla.insertRow(fila)
            
            # Formatear fecha y hora de manera segura como hacías en Jinja
            fecha_str = s.fecha.strftime('%d/%m/%Y') if hasattr(s, 'fecha') and s.fecha else '-'
            hora_str = s.hora.strftime('%H:%M') if hasattr(s, 'hora') and s.hora else '-'
            especialista = s.especialista if s.especialista else '-'
            comentarios = s.comentarios if s.comentarios else '-'
            
            # Crear los ítems de las celdas
            item_fecha = QTableWidgetItem(fecha_str)
            item_hora = QTableWidgetItem(hora_str)
            item_especialista = QTableWidgetItem(especialista)
            item_comentarios = QTableWidgetItem(comentarios)
            
            # Insertar ítems en sus respectivas columnas
            tabla.setItem(fila, 0, item_fecha)
            tabla.setItem(fila, 1, item_hora)
            tabla.setItem(fila, 2, item_especialista)
            tabla.setItem(fila, 3, item_comentarios)