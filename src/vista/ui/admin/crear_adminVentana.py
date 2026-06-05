import os
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtUiTools import loadUiType

# CORRECCIÓN: El .ui y el .py están juntos en la misma carpeta
ui_file = os.path.join(os.path.dirname(__file__), "crear_admin.ui")
ui_formulario, _ = loadUiType(ui_file)

class CrearAdminVentana(QDialog, ui_formulario):
    def __init__(self):
        super().__init__()
        
        # Inicializa y dibuja la interfaz en 'self'
        self.setupUi(self)
        
        # 🌟 NUEVO: Conectar los botones de tu archivo .ui para que la ventana responda
        self.btn_crear.clicked.connect(self.accept)     # Cierra devolviendo Código 1 (Aceptar)
        self.btn_cancelar.clicked.connect(self.reject)  # Cierra devolviendo Código 0 (Cancelar)
        
        # Restricciones visuales (Validadores en la Vista)
        self.configurar_restricciones()

    def configurar_restricciones(self):
        """Aplica filtros para que el usuario no escriba datos incorrectos"""
        # El teléfono solo puede tener números (9 dígitos máximo)
        regex_tel = QRegularExpression(r"^\d{0,9}$")
        validador_tel = QRegularExpressionValidator(regex_tel, self)
        self.txt_telefono.setValidator(validador_tel)
        
        # El DNI obliga a meter 8 números y una letra
        regex_dni = QRegularExpression(r"^\d{0,8}[a-zA-Z]?$")
        validador_dni = QRegularExpressionValidator(regex_dni, self)
        self.txt_dni.setValidator(validador_dni)

    def obtener_datos_formulario(self) -> dict:
        """
        Recolecta los datos de los campos mapeados correctamente con el .ui.
        La vista sigue siendo ciega y respeta el MVC puro.
        """
        return {
            "nombre": self.txt_nombre.text().strip(),   
            "nombreUsuario": self.txt_usuario.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "password": self.txt_password.text().strip()
        }

    def limpiar_formulario(self):
        """Vacía las cajas de texto tras crear el usuario o al cancelar."""
        self.txt_nombre.clear()     
        self.txt_usuario.clear()  
        self.txt_dni.clear()
        self.txt_telefono.clear()
        self.txt_email.clear()
        self.txt_password.clear()
        # Ponemos el cursor (foco) en la primera caja para mayor comodidad
        self.txt_nombre.setFocus()  