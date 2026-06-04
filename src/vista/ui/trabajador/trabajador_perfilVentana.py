import os
from datetime import datetime
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

# Cargamos el archivo .ui apuntando a su nombre exclusivo de trabajador
ui_path = os.path.join(os.path.dirname(__file__), "ui", "trabajador_perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorPerfilVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Configuraciones de diseño iniciales
        self.txt_telefono.setPlaceholderText("666777888")
        self.txt_password.setPlaceholderText("Dejar en blanco para no cambiar")

    def cargar_datos_perfil(self, usuario: dict):
        """
        Inyecta los datos del modelo/diccionario del trabajador en los componentes.
        """
        self.txt_nombre.setText(usuario.get("nombre", ""))
        self.txt_usuario.setText(usuario.get("nombreUsuario", ""))
        self.txt_dni.setText(usuario.get("dni", ""))
        self.txt_telefono.setText(usuario.get("telefono", ""))
        self.txt_email.setText(usuario.get("email", ""))
        
        # Siempre limpiamos el campo de contraseña al cargar la vista
        self.txt_password.clear()
        
        # Mapeo y conversión segura de la fecha de nacimiento
        fecha_bd = usuario.get("fechaNacimiento")
        if fecha_bd:
            if isinstance(fecha_bd, str):
                fecha_obj = datetime.strptime(fecha_bd, "%Y-%m-%d").date()
            else:
                fecha_obj = fecha_bd
                
            self.date_nacimiento.setDate(QDate(fecha_obj.year, fecha_obj.month, fecha_obj.day))
        else:
            self.date_nacimiento.setDate(QDate.currentDate())

    def obtener_datos_formulario(self) -> dict:
        """
        Recolecta el contenido actual de los inputs para simular el envío del formulario POST.
        """
        fecha_qdate = self.date_nacimiento.date()
        fecha_str = f"{fecha_qdate.year()}-{fecha_qdate.month():02d}-{fecha_qdate.day():02d}"
        
        datos = {
            "nombre": self.txt_nombre.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "fechaNacimiento": fecha_str
        }
        
        # Gestión de la contraseña opcional
        password_nueva = self.txt_password.text().strip()
        if password_nueva:
            datos["password"] = password_nueva
            
        return datos