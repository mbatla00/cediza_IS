import os
from datetime import date, datetime
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

ui_path = os.path.join(os.path.dirname(__file__), "sesiones.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteSesionesVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self.btn_volver.clicked.connect(self.close)
        self._configurar_tablas()
        self._cargar_datos()
        self.showMaximized()

    def _configurar_tablas(self):
        for tabla in [self.tabla_proximas, self.tabla_pasadas]:
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setVisible(True)
            header.setMinimumHeight(35)
            tabla.verticalHeader().setVisible(False)
            tabla.setRowCount(0)

    def _cargar_datos(self):
        # Corregido: Llamamos a la versión que retorna diccionarios básicos
        sesiones = self._controller.listar_sesiones_dict()
        
        hoy = date.today()
        proximas = []
        pasadas  = []

        for s in (sesiones or []):
            fecha_str = s.get('fecha', '')
            if not fecha_str or fecha_str == 'None':
                continue
            
            # Convertimos el string ('YYYY-MM-DD') a objeto date de forma segura para comparar
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                continue 

            if fecha_obj >= hoy:
                proximas.append(s)
            else:
                pasadas.append(s)

        self._rellenar_tabla(self.tabla_proximas, proximas, "No tienes sesiones próximas programadas.")
        self._rellenar_tabla(self.tabla_pasadas, pasadas, "No tienes sesiones pasadas.")

    def _rellenar_tabla(self, tabla, lista_sesiones, mensaje_vacio):
        tabla.setRowCount(0)

        if not lista_sesiones:
            tabla.setRowCount(1)
            tabla.setSpan(0, 0, 1, 4) 
            item = QTableWidgetItem(mensaje_vacio)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(0, 0, item)
            return

        for fila, s in enumerate(lista_sesiones):
            tabla.insertRow(fila)
            
            # Al ser un diccionario, extraemos de forma limpia con .get()
            fecha_val = s.get('fecha', '-')
            hora_val = s.get('hora', '-')
            especialista = s.get('especialista', '-')
            comentarios = s.get('comentarios', '-')

            # Opcional: Cambiar formato visual de YYYY-MM-DD a DD/MM/YYYY para el usuario
            try:
                fecha_obj = datetime.strptime(fecha_val, '%Y-%m-%d')
                fecha_val = fecha_obj.strftime('%d/%m/%Y')
            except (ValueError, TypeError):
                pass

            tabla.setItem(fila, 0, QTableWidgetItem(str(fecha_val)))
            tabla.setItem(fila, 1, QTableWidgetItem(str(hora_val)))
            tabla.setItem(fila, 2, QTableWidgetItem(str(especialista)))
            tabla.setItem(fila, 3, QTableWidgetItem(str(comentarios)))