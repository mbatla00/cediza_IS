import os
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtUiTools import loadUiType

ui_file = os.path.join(os.path.dirname(__file__), "crear_admin.ui")
ui_formulario, _ = loadUiType(ui_file)

class CrearAdminVentana(QDialog, ui_formulario):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador

        self.btn_crear.clicked.connect(self.procesar_guardado)
        self.btn_cancelar.clicked.connect(self.reject)

        self.configurar_restricciones()

    def configurar_restricciones(self):
        regex_tel = QRegularExpression(r"^\d{0,9}$")
        self.txt_telefono.setValidator(QRegularExpressionValidator(regex_tel, self))

        regex_dni = QRegularExpression(r"^\d{0,8}[a-zA-Z]?$")
        self.txt_dni.setValidator(QRegularExpressionValidator(regex_dni, self))

    def obtener_datos_formulario(self) -> dict:
        return {
            "nombre_completo": self.txt_nombre_completo.text().strip(),
            "nombre_usuario":  self.txt_nombre_usuario.text().strip(),
            "dni":             self.txt_dni.text().strip(),
            "telefono":        self.txt_telefono.text().strip(),
            "email":           self.txt_email.text().strip(),
            "password":        self.txt_password.text().strip()
        }

    def limpiar_formulario(self):
        self.txt_nombre_completo.clear()
        self.txt_nombre_usuario.clear()
        self.txt_dni.clear()
        self.txt_telefono.clear()
        self.txt_email.clear()
        self.txt_password.clear()

    def procesar_guardado(self):
        datos = self.obtener_datos_formulario()

        if not datos["nombre_completo"] or not datos["nombre_usuario"] or not datos["dni"]:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, rellena los campos obligatorios.")
            return

        exito, msg, _ = self.controlador.agregar_administrador(datos)

        if exito:
            QMessageBox.information(self, "Éxito", f"Administrador '{datos['nombre_completo']}' registrado correctamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error al crear", f"No se pudo registrar: {msg}")