import os
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

ui_path = os.path.join(os.path.dirname(__file__), "admin_perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class AdminPerfilVentana(QMainWindow, Ui_MainWindow):
    """
    Ventana encargada de mostrar y editar el perfil de un usuario Administrador.
    Permite cambiar datos personales, validar restricciones temporales y gestionar
    contraseñas de manera segura sin sobreescribirlas accidentalmente.
    """
    def __init__(self, controlador, nombre_usuario_actual):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        self.nombre_usuario_actual = nombre_usuario_actual
        
        self.txt_telefono.setPlaceholderText("666777888")
        self.txt_password.setPlaceholderText("Dejar en blanco para no cambiar")
        self.txt_usuario.setReadOnly(True)
        self.txt_usuario.setStyleSheet("background-color: #e9ecef; color: #6c757d;")

        # Conexión interna
        if hasattr(self, 'btn_guardar'):
            self.btn_guardar.clicked.connect(self.procesar_guardado)
        
        if hasattr(self, 'btn_volver'):
            self.btn_volver.clicked.connect(self.close)
        elif hasattr(self, 'btn_cancelar'):
            self.btn_cancelar.clicked.connect(self.close)

        # Autocargar los datos nada más abrirse
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        # Pedimos los datos en formato diccionario (limpio)
        datos_dict = self.controlador.obtener_usuario_dict(self.nombre_usuario_actual)
        
        if datos_dict:
            # Rellenamos la vista con el diccionario, sin guardar el VO
            self.cargar_datos_perfil(datos_dict)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron cargar los datos de la cuenta.")

    def cargar_datos_perfil(self, usuario: dict):
        # Obtenemos el nombre para usarlo tanto en la caja de texto como en el título
        nombre_real = usuario.get("nombre", "")
        
        # ACTUALIZAMOS EL TÍTULO DE BIENVENIDA AQUÍ
        self.lbl_titulo.setText(f"Bienvenido de nuevo, {nombre_real}")
        
        self.txt_nombre.setText(nombre_real)
        self.txt_usuario.setText(usuario.get("nombreUsuario", ""))
        self.txt_dni.setText(usuario.get("dni", ""))
        self.txt_email.setText(usuario.get("email", ""))
        self.txt_telefono.setText(usuario.get("telefono", ""))

        fecha_bd = usuario.get("fechaNacimiento")
        if fecha_bd:
            if isinstance(fecha_bd, str):
                fecha_obj = datetime.strptime(fecha_bd, "%Y-%m-%d").date()
            else:
                fecha_obj = fecha_bd 
            qdate = QDate(fecha_obj.year, fecha_obj.month, fecha_obj.day)
            self.date_nacimiento.setDate(qdate)
        else:
            self.date_nacimiento.setDate(QDate.currentDate())

    def obtener_datos_formulario(self) -> dict:
        fecha_qdate = self.date_nacimiento.date()
        fecha_str = f"{fecha_qdate.year()}-{fecha_qdate.month():02d}-{fecha_qdate.day():02d}"
        
        return {
            "nombre": self.txt_nombre.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "telefono": self.txt_telefono.text().strip(),
            "email": self.txt_email.text().strip(),
            "fechaNacimiento": fecha_str,
            "password": self.txt_password.text().strip() # El DAO decidirá si actualizarla según si está vacía
        }

    def procesar_guardado(self):
        datos_formulario = self.obtener_datos_formulario()

        fecha_nacimiento_str = datos_formulario.get("fechaNacimiento")
        if fecha_nacimiento_str:
            # Convertimos el string "yyyy-MM-dd" a un objeto date para poder comparar
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
            fecha_actual = datetime.now().date()
            
            if fecha_nacimiento > fecha_actual:
                QMessageBox.warning(self, "Error de validación", "La fecha de nacimiento no puede ser una fecha futura.")
                return 
        
        # Enviamos al controlador solo el nombre de usuario (str) y los datos
        exito, msg = self.controlador.actualizar_usuario(self.nombre_usuario_actual, datos_formulario)
        
        if exito:
            QMessageBox.information(self, "Éxito", "Perfil actualizado correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {msg}")