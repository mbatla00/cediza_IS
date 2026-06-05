import os
from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import loadUiType

# 1. Cargar el diseño (mantenemos tu ruta dentro de la carpeta 'ui')
ruta_ui = os.path.join(os.path.dirname(__file__), "ui", "trabajador_form.ui")
Ui_Dialog, _ = loadUiType(ruta_ui)

class NuevoTrabajadorVentana(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 2. Estado inicial: ocultar el campo de especialidad
        self.lbl_especialidad.setVisible(False)
        self.txt_especialidad.setVisible(False)
        
        # 3. Conectar la señal del desplegable
        self.cb_tipo.currentTextChanged.connect(self.verificar_especialidad)
        
        # 4. 🌟 LO NUEVO: Conectar las acciones de tus botones de abajo
        self.btn_guardar.clicked.connect(self.accept)    # Cierra la ventana devolviendo "Aceptar"
        self.btn_cancelar.clicked.connect(self.reject)  # Cierra la ventana devolviendo "Cancelar"

    def verificar_especialidad(self, texto_seleccionado):
        """Muestra u oculta la especialidad dependiendo del tipo de trabajador"""
        if texto_seleccionado.lower() == "especialista":
            self.lbl_especialidad.setVisible(True)
            self.txt_especialidad.setVisible(True)
        else:
            self.lbl_especialidad.setVisible(False)
            self.txt_especialidad.setVisible(False)
            self.txt_especialidad.clear()  # Limpia el texto por seguridad si cambian de idea