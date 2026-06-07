import os
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtUiTools import loadUiType

ui_file = os.path.join(os.path.dirname(__file__), "crear_admin.ui")
ui_formulario, _ = loadUiType(ui_file)

class CrearAdminVentana(QDialog, ui_formulario):
    # AÑADIDO: Recibe el controlador
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        
        # Conexiones internas de la vista
        self.btn_crear.clicked.connect(self.procesar_guardado)
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.configurar_restricciones()

    def configurar_restricciones(self):
        regex_tel = QRegularExpression(r"^\d{0,9}$")
        validador_tel = QRegularExpressionValidator(regex_tel, self)
        self.txt_telefono.setValidator(validador_tel)
        
        regex_dni = QRegularExpression(r"^\d{0,8}[a-zA-Z]?$")
        validador_dni = QRegularExpressionValidator(regex_dni, self)
        self.txt_dni.setValidator(validador_dni)

    def obtener_datos_formulario(self) -> dict:
        return {
            "nombre": self.txt_nombre.text().strip(),   
            "nombreUsuario": self.txt_usuario.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "password": self.txt_password.text().strip()
        }

    def limpiar_formulario(self):
        self.txt_nombre.clear()     
        self.txt_usuario.clear()  
        self.txt_dni.clear()
        self.txt_telefono.clear()
        self.txt_email.clear()
        self.txt_password.clear()

    # AÑADIDO: Lógica de guardado interna
    def procesar_guardado(self):
        datos = self.obtener_datos_formulario()
        
        # Validaciones visuales rápidas
        if not datos["nombre"] or not datos["nombreUsuario"] or not datos["dni"]:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, rellena los campos obligatorios.")
            return

        # Llamamos al controlador de tus compañeros (Asegúrate de que este método exista en admin_controller.py
        # puede llamarse 'agregar_administrador', 'agregar_admin' o similar)
        exito, msg, _ = self.controlador.agregar_administrador(datos)
        
        if exito:
            QMessageBox.information(self, "Éxito", f"Administrador '{datos['nombre']}' registrado correctamente.")
            self.accept() # Cierra la ventana y devuelve éxito
        else:
            QMessageBox.warning(self, "Error al crear", f"No se pudo registrar: {msg}")