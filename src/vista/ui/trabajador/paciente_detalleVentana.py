import os
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView
from PySide6.QtUiTools import loadUiType

ui_path = os.path.join(os.path.dirname(__file__), "paciente_detalle.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteDetalleVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador, nombre_usuario_paciente):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador
        self._nombre_paciente = nombre_usuario_paciente

        self._configurar_tabla()
        self._conectar_botones()
        self._cargar_datos()

    def _configurar_tabla(self):
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # --- LÍNEAS CORREGIDAS: Uso seguro de QAbstractItemView ---
        self.tabla_historial.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_historial.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def _conectar_botones(self):
        self.btn_volver.clicked.connect(self.close)
        self.btn_volver_2.clicked.connect(self.close)
        self.btn_evaluar.clicked.connect(self._abrir_evaluacion)
        self.btn_guardar_nota.clicked.connect(self._procesar_nueva_nota)
        self.btn_guardar_contacto.clicked.connect(self._procesar_nuevo_contacto)
        # Estos dos no hacen nada por ahora pero los conectamos para que no queden sueltos
        self.btn_tab_historial.clicked.connect(lambda: None)
        self.btn_tab_evaluar.clicked.connect(lambda: None)

    def _cargar_datos(self):
        paciente = self._controller.obtener_paciente(self._nombre_paciente)
        comentarios = self._controller.listar_comentarios_de_paciente(self._nombre_paciente)
        evaluaciones = self._controller.listar_evaluaciones_de_paciente(self._nombre_paciente)
        sesiones = self._controller.listar_sesiones_de_paciente(self._nombre_paciente)
        familiares = self._controller.listar_familiares_de_paciente(self._nombre_paciente)

        if paciente:
            self.txt_nombre.setText(getattr(paciente, 'nombre', ''))
            self.txt_dni.setText(getattr(paciente, 'dni', ''))
            self.txt_telefono.setText(getattr(paciente, 'telefono', '') or '')
            self.txt_asistencia.setText(getattr(paciente, 'tipo', '') or '')
            self.txt_diagnostico.setText(getattr(paciente, 'diagnostico', '') or '')

        historial = list(comentarios or []) + list(evaluaciones or [])
        self._rellenar_historial(historial)
        self._rellenar_contactos(familiares or [])
        self._rellenar_sesiones(sesiones or [])

    def _rellenar_historial(self, historial):
        self.tabla_historial.setRowCount(0)
        for fila, nota in enumerate(historial):
            self.tabla_historial.insertRow(fila)
            fecha = getattr(nota, 'dia', "")
            autor = getattr(nota, 'auxiliar', "")
            
            if hasattr(nota, 'nota'):
                contenido = getattr(nota, 'nota', "")
            else:
                emocional = getattr(nota, 'estadoEmocional', "-")
                movilidad = getattr(nota, 'movilidad', "-")
                apetito = getattr(nota, 'apetito', "-")
                obs = getattr(nota, 'observaciones', "")
                contenido = (
                    f"[EVALUACIÓN] Emocional: {emocional}/5 | "
                    f"Movilidad: {movilidad}/5 | "
                    f"Apetito: {apetito}/5\n"
                    f"Obs: {obs}"
                )
            
            self.tabla_historial.setItem(fila, 0, QTableWidgetItem(str(fecha)))
            self.tabla_historial.setItem(fila, 1, QTableWidgetItem(str(autor)))
            self.tabla_historial.setItem(fila, 2, QTableWidgetItem(str(contenido)))

    def _rellenar_contactos(self, contactos):
        self.lista_contactos.clear()
        if contactos:
            self.lbl_status_contactos.hide()
            self.lista_contactos.show()
            for c in contactos:
                self.lista_contactos.addItem(
                    f"👤 {getattr(c, 'nombre', '')} - 📞 {getattr(c, 'telefono', '')}"
                )
        else:
            self.lbl_status_contactos.show()
            self.lista_contactos.hide()

    def _rellenar_sesiones(self, sesiones):
        self.lista_sesiones.clear()
        for s in (sesiones or []):
            self.lista_sesiones.addItem(
                f"📅 {getattr(s, 'fecha', '')} {getattr(s, 'hora', '')}"
            )

    def _procesar_nueva_nota(self):
        texto = self.txt_nueva_nota.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Atención", "La nota no puede estar vacía.")
            return
        exito, msg = self._controller.agregar_comentario(self._nombre_paciente, texto)
        if exito:
            self.txt_nueva_nota.clear()
            QMessageBox.information(self, "Éxito", "Nota añadida al expediente.")
            self._cargar_datos()
        else:
            QMessageBox.warning(self, "Error", msg)

    def _procesar_nuevo_contacto(self):
        nombre = self.txt_contacto_nombre.text().strip()
        parentesco = self.txt_contacto_parentesco.text().strip()
        telefono = self.txt_contacto_telefono.text().strip()
        if not nombre:
            return
        
        # Si el controlador tiene este método, quita el '#' para descomentarlo en el futuro:
        # self._controller.agregar_familiar(self._nombre_paciente, nombre, parentesco, telefono)
        
        self.txt_contacto_nombre.clear()
        self.txt_contacto_parentesco.clear()
        self.txt_contacto_telefono.clear()

    def _abrir_evaluacion(self):
        from src.vista.ui.trabajador.evaluar_pacienteVentana import EvaluarPacienteVentana
        self._eval = EvaluarPacienteVentana(self._controller, self._nombre_paciente)
        self._eval.show()