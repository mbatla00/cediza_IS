import os
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

ui_path = os.path.join(os.path.dirname(__file__), "trabajador_perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class TrabajadorPerfilVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self._controller = controlador

        self.txt_telefono.setPlaceholderText("666777888")
        self.txt_password.setPlaceholderText("Dejar en blanco para no cambiar")
        self.txt_usuario.setReadOnly(True)

        self.btn_guardar.clicked.connect(self._procesar_guardado)
        self.btn_volver.clicked.connect(self.close)

        self._cargar_datos()

    def _cargar_datos(self):
        datos = self._controller.obtener_trabajador_dict()
        if datos:
            
            self._rellenar_formulario(datos)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron cargar los datos.")

    def _rellenar_formulario(self, usuario: dict):
        self.txt_nombre.setText(usuario.get("nombre", ""))
        self.txt_usuario.setText(usuario.get("nombreUsuario", ""))
        self.txt_dni.setText(usuario.get("dni", ""))
        self.txt_telefono.setText(usuario.get("telefono", ""))
        self.txt_email.setText(usuario.get("email", ""))
        self.txt_password.clear()

        fecha_bd = usuario.get("fechaNacimiento")
        if fecha_bd:
            if isinstance(fecha_bd, str):
                fecha_obj = datetime.strptime(fecha_bd, "%Y-%m-%d").date()
            else:
                fecha_obj = fecha_bd
            self.date_nacimiento.setDate(QDate(fecha_obj.year, fecha_obj.month, fecha_obj.day))
        else:
            self.date_nacimiento.setDate(QDate.currentDate())

    def _obtener_datos_formulario(self) -> dict:
        datos = {
            "nombre": self.txt_nombre.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "fechaNacimiento": self.date_nacimiento.date().toString("yyyy-MM-dd")
        }
        password = self.txt_password.text().strip()
        if password:
            datos["password"] = password
        return datos

    def _procesar_guardado(self):
        datos = self._obtener_datos_formulario()
        
        # El controlador ya sabe a quién actualizar gracias a su estado interno
        exito, msg = self._controller.actualizar_trabajador(datos)
        
        if exito:
            QMessageBox.information(self, "Éxito", "Perfil actualizado correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {msg}")