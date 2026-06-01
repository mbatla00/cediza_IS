import os
from datetime import datetime
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

# Cargar el archivo .ui del perfil del admin
ui_path = os.path.join(os.path.dirname(__file__), "ui", "admin", "perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class AdminPerfilVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Opcional: Poner placeholders como en el HTML
        self.txt_telefono.setPlaceholderText("666777888")
        self.txt_password.setPlaceholderText("Dejar en blanco para no cambiar")

    def cargar_datos_perfil(self, usuario: dict):
        """
        Rellena el formulario con los datos actuales del administrador.
        """
        self.txt_nombre.setText(usuario.get("nombre", ""))
        self.txt_usuario.setText(usuario.get("nombreUsuario", ""))
        self.txt_dni.setText(usuario.get("dni", ""))
        self.txt_telefono.setText(usuario.get("telefono", ""))
        self.txt_email.setText(usuario.get("email", ""))
        
        # Limpiar campo de contraseña por seguridad
        self.txt_password.clear()
        
        # Manejar la fecha de nacimiento (de string/datetime de tu BD a QDate de Qt)
        fecha_bd = usuario.get("fechaNacimiento")
        if fecha_bd:
            # Asumiendo que llega como un objeto datetime de Python o string 'YYYY-MM-DD'
            if isinstance(fecha_bd, str):
                fecha_obj = datetime.strptime(fecha_bd, "%Y-%m-%d").date()
            else:
                fecha_obj = fecha_bd # Si ya es tipo date/datetime
                
            qdate = QDate(fecha_obj.year, fecha_obj.month, fecha_obj.day)
            self.date_nacimiento.setDate(qdate)
        else:
            self.date_nacimiento.setDate(QDate.currentDate())

    def obtener_datos_formulario(self) -> dict:
        """
        Recolecta los datos de los campos de texto para enviarlos al controlador 
        cuando se pulsa 'Guardar Cambios'.
        """
        # Extraer la fecha del QDateEdit y pasarla a string YYYY-MM-DD
        fecha_qdate = self.date_nacimiento.date()
        fecha_str = f"{fecha_qdate.year()}-{fecha_qdate.month():02d}-{fecha_qdate.day():02d}"
        
        datos = {
            "nombre": self.txt_nombre.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "fechaNacimiento": fecha_str
        }
        
        # Solo enviamos la contraseña si el usuario escribió algo
        password_nueva = self.txt_password.text().strip()
        if password_nueva:
            datos["password"] = password_nueva
            
        return datos