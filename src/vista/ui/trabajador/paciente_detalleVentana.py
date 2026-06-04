import os
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import loadUiType

# Localizamos de forma segura el archivo .ui que acabas de guardar
# Ajusta "ui" si tu carpeta de diseños se llama de otra forma
UI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
ui_path = os.path.join(UI_DIR, "paciente_detalle.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacienteDetalleVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.configurar_tabla()

    def configurar_tabla(self):
        """Configura el comportamiento visual de la tabla de historial clínico"""
        header = self.tabla_historial.horizontalHeader()
        # La fecha y el autor ocupan solo lo que necesitan
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        # La columna de la nota/contenido se estira para ocupar todo el espacio restante
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Hace que al hacer clic se seleccione la fila entera y no celdas sueltas
        self.tabla_historial.setSelectionBehavior(self.tabla_historial.SelectionBehavior.SelectRows)

    def cargar_datos_paciente(self, paciente: dict, historial: list):
        """
        Pinta los datos del paciente y su historial en la interfaz.
        Mapeado directamente con tu modelo de dominio.
        """
        # 1. Rellenar los campos de texto estáticos (bloqueados en ReadOnly desde el .ui)
        nombre_completo = f"{paciente.get('nombre', '')} {paciente.get('apellidos', '')}".strip()
        self.txt_nombre.setText(nombre_completo if nombre_completo else "No registrado")
        self.txt_dni.setText(paciente.get('dni', '---'))
        self.txt_asistencia.setText(paciente.get('tipoAsistencia', 'No especificado'))
        self.txt_diagnostico.setPlainText(paciente.get('diagnostico', 'Sin diagnóstico registrado.'))

        # 2. Vaciar y repoblar la tabla del historial clínico
        self.tabla_historial.setRowCount(0)
        
        for fila, elemento in enumerate(historial):
            self.tabla_historial.insertRow(fila)
            
            # Extraemos los campos comunes adaptándonos a tu modelo de dominio
            fecha = elemento.get("fechaHora", elemento.get("fecha", "---"))
            autor = elemento.get("trabajador", "Personal del Centro")
            
            # Diferenciamos si el elemento es una 'NotaLibre' o una 'Evaluación Profesional'
            if "contenido" in elemento:
                # Es una Nota Libre
                contenido_nota = elemento.get("contenido", "")
            else:
                # Es una Evaluación Profesional (tiene estadoEmocional, movilidad, apetito)
                emocional = elemento.get("estadoEmocional", "-")
                movilidad = elemento.get("movilidad", "-")
                apetito = elemento.get("apetito", "-")
                obs = elemento.get("observaciones", "")
                
                contenido_nota = (
                    f"[EVALUACIÓN] Emocional: {emocional}/5 | "
                    f"Movilidad: {movilidad}/5 | "
                    f"Apetito: {apetito}/5\n"
                    f"Obs: {obs}"
                )
            
            # Insertamos los textos en cada celda de la fila actual
            self.tabla_historial.setItem(fila, 0, QTableWidgetItem(str(fecha)))
            self.tabla_historial.setItem(fila, 1, QTableWidgetItem(str(autor)))
            self.tabla_historial.setItem(fila, 2, QTableWidgetItem(str(contenido_nota)))