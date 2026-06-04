import os
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QPushButton, 
                               QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate, QTime

ui_path = os.path.join(os.path.dirname(__file__), "ui", "especialista_dashboard.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class EspecialistaDashboardVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Configuración inicial de la UI
        self.date_fecha.setDate(QDate.currentDate())
        self.time_hora.setTime(QTime.currentTime())
        
        self.configurar_tablas()
        
        # Conexiones de botones principales
        self.btn_crear_sesion.clicked.connect(self.procesar_nueva_sesion)
        # self.btn_volver.clicked.connect(self.cerrar_y_volver) # A implementar en tu controlador

    def configurar_tablas(self):
        """ Configura las cabeceras y el comportamiento de las tablas """
        columnas = ["Fecha", "Hora", "Paciente", "Comentarios", "Acciones"]
        
        for tabla in [self.tabla_proximas, self.tabla_pasadas]:
            tabla.setColumnCount(len(columnas))
            tabla.setHorizontalHeaderLabels(columnas)
            # Hacer que las columnas se expandan, excepto las de acciones y fecha/hora
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(2, QHeaderView.Stretch) # Paciente
            header.setSectionResizeMode(3, QHeaderView.Stretch) # Comentarios
            tabla.setEditTriggers(QTableWidget.NoEditTriggers) # Solo lectura
            tabla.setSelectionBehavior(QTableWidget.SelectRows)

    def cargar_datos(self, nombre_especialista: str, pacientes: list, sesiones_proximas: list, sesiones_pasadas: list):
        """ Recibe los datos del controlador y rellena la interfaz """
        self.lbl_subtitulo.setText(f"Bienvenido/a, {nombre_especialista}. Gestiona tus sesiones y pacientes.")
        
        # Cargar ComboBox de pacientes
        self.cmb_paciente.clear()
        self.cmb_paciente.addItem("-- Seleccionar paciente --", None)
        for p in pacientes:
            texto = f"{p['nombre']} ({p['nombreUsuario']})"
            self.cmb_paciente.addItem(texto, p['nombreUsuario']) # userData = nombreUsuario
            
        # Cargar tablas
        self.rellenar_tabla(self.tabla_proximas, sesiones_proximas, es_pasada=False)
        self.rellenar_tabla(self.tabla_pasadas, sesiones_pasadas, es_pasada=True)

    def rellenar_tabla(self, tabla, sesiones: list, es_pasada: bool):
        tabla.setRowCount(0)
        for i, s in enumerate(sesiones):
            tabla.insertRow(i)
            
            # Datos de texto
            tabla.setItem(i, 0, QTableWidgetItem(s.get("fecha", "-")))
            tabla.setItem(i, 1, QTableWidgetItem(s.get("hora", "-")))
            tabla.setItem(i, 2, QTableWidgetItem(s.get("paciente", "-")))
            tabla.setItem(i, 3, QTableWidgetItem(s.get("comentarios", "-")))
            
            # Contenedor para los botones de acción
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout(widget_acciones)
            layout_acciones.setContentsMargins(2, 2, 2, 2)
            layout_acciones.setSpacing(5)
            
            # Botón Ver (Ambas tablas)
            btn_ver = QPushButton("👁️ Ver")
            btn_ver.clicked.connect(lambda checked, p=s.get("paciente"): self.abrir_detalle_paciente(p))
            layout_acciones.addWidget(btn_ver)
            
            if not es_pasada:
                # Botones Editar y Eliminar (Solo próximas)
                btn_editar = QPushButton("✏️ Editar")
                btn_editar.clicked.connect(lambda checked, id_s=s.get("idSesion"): self.abrir_editar_sesion(id_s))
                
                btn_eliminar = QPushButton("🗑️ Eliminar")
                btn_eliminar.setStyleSheet("background-color: #dc3545; color: white;")
                btn_eliminar.clicked.connect(lambda checked, id_s=s.get("idSesion"), p=s.get("paciente"), f=s.get("fecha"): self.confirmar_eliminar(id_s, p, f))
                
                layout_acciones.addWidget(btn_editar)
                layout_acciones.addWidget(btn_eliminar)
                
            tabla.setCellWidget(i, 4, widget_acciones)
            # Ajustar la altura de la fila para que quepan los botones
            tabla.setRowHeight(i, 40)

    # --- ACCIONES ---
    def procesar_nueva_sesion(self):
        # El userData almacena el nombreUsuario que asignamos al cargar el ComboBox
        paciente_usuario = self.cmb_paciente.currentData() 
        
        if not paciente_usuario:
            QMessageBox.warning(self, "Error", "Debe seleccionar un paciente.")
            return
            
        payload = {
            "paciente": paciente_usuario,
            "fecha": self.date_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.time_hora.time().toString("HH:mm"),
            "comentarios": self.txt_comentarios.toPlainText()
        }
        
        print("Enviando al controlador para crear sesión:", payload)
        # Aquí llamarías a tu controlador: self.controlador.crear_sesion(payload)
        QMessageBox.information(self, "Éxito", "Sesión programada correctamente.")
        
        # Limpiar formulario tras guardar
        self.cmb_paciente.setCurrentIndex(0)
        self.txt_comentarios.clear()

    def confirmar_eliminar(self, id_sesion, paciente, fecha):
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Estás seguro de eliminar la sesión del paciente {paciente} del día {fecha}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            print(f"Llamando al controlador para eliminar sesión ID: {id_sesion}")
            # self.controlador.eliminar_sesion(id_sesion)
            # self.recargar_datos() # Volver a pedir datos a la BD

    def abrir_detalle_paciente(self, paciente_usuario):
        print(f"Abriendo vista detalle para el paciente: {paciente_usuario}")

    def abrir_editar_sesion(self, id_sesion):
        print(f"Abriendo ventana de edición para la sesión: {id_sesion}")