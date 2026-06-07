import os
import matplotlib
# Le decimos a matplotlib que use el motor de Qt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
        self._crear_grafico() 
        self._conectar_botones()
        self._cargar_datos()

    def _configurar_tabla(self):
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.tabla_historial.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_historial.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def _crear_grafico(self):
        self.figura = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figura)
        self.ax = self.figura.add_subplot(111)

        if hasattr(self, 'layout_grafico'):
            self.layout_grafico.addWidget(self.canvas)
        else:
            print("AVISO: No se encontró 'layout_grafico' en el diseño .ui")

    def _conectar_botones(self):
        self.btn_volver.clicked.connect(self.close)
        self.btn_volver_2.clicked.connect(self.close)
        self.btn_evaluar.clicked.connect(self._abrir_evaluacion)
        self.btn_guardar_nota.clicked.connect(self._procesar_nueva_nota)
        self.btn_guardar_contacto.clicked.connect(self._procesar_nuevo_contacto)

    def _cargar_datos(self):
        # Usamos los nuevos métodos que devuelven diccionarios
        paciente = self._controller.obtener_paciente_dict(self._nombre_paciente)
        comentarios = self._controller.listar_comentarios_dict(self._nombre_paciente)
        evaluaciones = self._controller.listar_evaluaciones_dict(self._nombre_paciente)
        sesiones = self._controller.listar_sesiones_de_paciente_dict(self._nombre_paciente)
        familiares = self._controller.listar_familiares_dict(self._nombre_paciente)

        if paciente:
            self.txt_nombre.setText(paciente.get('nombre', ''))
            self.txt_dni.setText(paciente.get('dni', ''))
            self.txt_telefono.setText(paciente.get('telefono', ''))
            self.txt_asistencia.setText(paciente.get('tipo', ''))
            self.txt_diagnostico.setText(paciente.get('diagnostico', ''))

        historial = list(comentarios or []) + list(evaluaciones or [])
        self._rellenar_historial(historial)
        self._rellenar_contactos(familiares or [])
        self._rellenar_sesiones(sesiones or [])
        
        self._dibujar_grafico(evaluaciones or [])

    def _dibujar_grafico(self, evaluaciones):
        self.ax.clear()

        # Filtramos diccionarios que tengan la clave 'estadoEmocional'
        evals_validas = [e for e in evaluaciones if 'estadoEmocional' in e]

        if not evals_validas:
            self.ax.text(0.5, 0.5, "No hay suficientes evaluaciones\npara mostrar la gráfica.",
                         ha='center', va='center', color='gray', fontsize=10)
            self.ax.axis('off')
            self.canvas.draw()
            return

        self.ax.axis('on')
        # Ordenamos usando .get() en lugar de getattr()
        evals_validas.sort(key=lambda x: str(x.get('dia', x.get('fecha', ''))))

        fechas, emocional, movilidad, apetito = [], [], [], []

        for ev in evals_validas:
            fecha_eval = ev.get('dia', ev.get('fecha', 'Sin fecha'))
            fechas.append(str(fecha_eval))
            
            emocional.append(int(ev.get('estadoEmocional', 0)))
            movilidad.append(int(ev.get('movilidad', 0)))
            apetito.append(int(ev.get('apetito', 0)))

        self.ax.plot(fechas, emocional, label='Emocional', marker='o', color='#0d6efd')
        self.ax.plot(fechas, movilidad, label='Movilidad', marker='s', color='#198754')
        self.ax.plot(fechas, apetito, label='Apetito', marker='^', color='#dc3545')

        self.ax.set_ylim(0.5, 5.5)
        self.ax.set_yticks([1, 2, 3, 4, 5])
        
        self.ax.set_ylabel("Puntuación (1-5)")
        self.ax.set_xlabel("Fechas de Evaluación")
        
        self.ax.legend(fontsize=8)
        self.ax.grid(True, linestyle='--', alpha=0.5)

        self.figura.autofmt_xdate(rotation=45)
        self.figura.tight_layout()

        self.canvas.draw()

    def _rellenar_historial(self, historial):
        self.tabla_historial.setRowCount(0)
        
        # Ordenamos usando .get()
        historial_ordenado = sorted(
            historial, 
            key=lambda x: str(x.get('dia', x.get('fecha', ''))), 
            reverse=True
        )
        
        for fila, nota in enumerate(historial_ordenado):
            self.tabla_historial.insertRow(fila)
            
            fecha = nota.get('dia', nota.get('fecha', "Sin fecha"))
            autor = nota.get('auxiliar', nota.get('trabajador', "Desconocido"))
            
            if 'nota' in nota:
                contenido = nota.get('nota', "")
            else:
                emocional = nota.get('estadoEmocional', "-")
                movilidad = nota.get('movilidad', "-")
                apetito = nota.get('apetito', "-")
                obs = nota.get('observaciones', "")
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
                    f"👤 {c.get('nombre', '')} - 📞 {c.get('telefono', '')}"
                )
        else:
            self.lbl_status_contactos.show()
            self.lista_contactos.hide()

    def _rellenar_sesiones(self, sesiones):
        self.lista_sesiones.clear()
        for s in (sesiones or []):
            self.lista_sesiones.addItem(
                f"📅 {s.get('fecha', '')} {s.get('hora', '')}"
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
            QMessageBox.warning(self, "Atención", "El nombre del contacto es obligatorio.")
            return
        
        self._controller.agregar_familiar(self._nombre_paciente, nombre, parentesco, telefono)
        
        self.txt_contacto_nombre.clear()
        self.txt_contacto_parentesco.clear()
        self.txt_contacto_telefono.clear()
        
        self._cargar_datos()
        QMessageBox.information(self, "Éxito", "Contacto de emergencia guardado correctamente.")

    def _abrir_evaluacion(self):
        from src.vista.ui.trabajador.evaluar_pacienteVentana import EvaluarPacienteVentana
        self._eval = EvaluarPacienteVentana(self._controller, self._nombre_paciente)
        self._eval.show()