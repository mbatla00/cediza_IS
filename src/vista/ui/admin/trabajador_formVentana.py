import os
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import loadUiType

ruta_ui = os.path.join(os.path.dirname(__file__), "trabajador_form.ui")
Ui_Dialog, _ = loadUiType(ruta_ui)

class NuevoTrabajadorVentana(QDialog, Ui_Dialog):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        
        self.lbl_especialidad.setVisible(False)
        self.txt_especialidad.setVisible(False)
        
        self.cb_tipo.currentTextChanged.connect(self.verificar_especialidad)
        
        # Conexión interna de botones
        self.btn_guardar.clicked.connect(self.procesar_guardado)    
        self.btn_cancelar.clicked.connect(self.reject)  

    def verificar_especialidad(self, texto_seleccionado):
        if texto_seleccionado.lower() == "especialista":
            self.lbl_especialidad.setVisible(True)
            self.txt_especialidad.setVisible(True)
        else:
            self.lbl_especialidad.setVisible(False)
            self.txt_especialidad.setVisible(False)
            self.txt_especialidad.clear()

    def obtener_datos_formulario(self) -> dict:
        return {
            "nombre": self.txt_nombre_completo.text().strip(),   # ← Corregido
            "usuario": self.txt_nombre_usuario.text().strip(),   # ← Corregido
            "dni": self.txt_dni.text().strip(),
            "telefono": "",                                      # ← Ajustado, ya no pide txt_telefono
            "email": self.txt_email.text().strip(),
            "password": self.txt_password.text().strip(),
            "tipo": self.cb_tipo.currentText().strip(),
            "especialidad": self.txt_especialidad.text().strip()
        }

    def procesar_guardado(self):
        # 1. Obtenemos datos crudos
        datos = self.obtener_datos_formulario()
        
        # 2. El controlador hace toda la magia y pone los valores por defecto
        exito, msg, _ = self.controlador.agregar_trabajador(datos)
        
        # 3. La vista solo muestra mensajes
        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", msg)