import os
from PySide6.QtWidgets import QDialog, QTableWidgetItem
from PySide6.QtUiTools import loadUiType

# 1. Cargar el diseño del PACIENTE
ruta_ui = os.path.join(os.path.dirname(__file__), "paciente_form.ui")
Ui_Dialog, _ = loadUiType(ruta_ui)

class CrearPacienteVentana(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 2. Conectar los botones de añadir a sus funciones
        self.btn_anadir_enfermedad.clicked.connect(self.anadir_enfermedad)
        self.btn_anadir_contacto.clicked.connect(self.anadir_contacto)
        
        # 3. Conectar botones principales
        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_guardar.clicked.connect(self.accept) 

    def anadir_enfermedad(self):
        """Añade la enfermedad escrita a la lista visual"""
        # Capturamos el texto de tu caja 'text_Enfermedad'
        enfermedad = self.text_Enfermedad.text().strip()
        
        if enfermedad:
            self.lista_enfermedades.addItem(enfermedad)
            self.text_Enfermedad.clear() # Limpiar la caja tras añadir

    def anadir_contacto(self):
        """Añade una nueva columna a la tabla de contactos 'Familiares'"""
        columna_actual = self.Familiares.columnCount()
        self.Familiares.insertColumn(columna_actual)
        
        # Crea celdas vacías listas para que el usuario haga doble clic y escriba
        self.Familiares.setItem(0, columna_actual, QTableWidgetItem(""))
        self.Familiares.setItem(1, columna_actual, QTableWidgetItem(""))
        self.Familiares.setItem(2, columna_actual, QTableWidgetItem(""))

    def obtener_datos_formulario(self) -> dict:
        """
        Recolecta los datos para el controlador respetando el MVC puro.
        Usa los nombres exactos que has definido en Qt Designer.
        """
        datos = {
            "nombre": self.texto_NombreCompleto.text().strip(),
            "nombreUsuario": self.text_Usuario.text().strip(),
            "dni": self.text_DNI.text().strip(),
            "fechaNacimiento": self.date_Nacimiento.date().toString("yyyy-MM-dd"),
            "telefono": self.text_Telefono.text().strip(),
            "email": self.text_email.text().strip(),
            "password": self.text_password.text().strip(),
            "tipoPaciente": self.tipo.currentText(),
            "cuentaBancaria": self.text_Cuenta_Bancaria.text().strip()
        }
        
        # Recoger también la lista de enfermedades dinámicas
        enfermedades = []
        for i in range(self.lista_enfermedades.count()):
            enfermedades.append(self.lista_enfermedades.item(i).text())
            
        datos["enfermedades"] = enfermedades

        return datos