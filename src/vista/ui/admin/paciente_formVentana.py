import os
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtUiTools import loadUiType

ruta_ui = os.path.join(os.path.dirname(__file__), "paciente_form.ui")
Ui_Dialog, _ = loadUiType(ruta_ui)

class CrearPacienteVentana(QDialog, Ui_Dialog):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        
        self.btn_anadir_enfermedad.clicked.connect(self.anadir_enfermedad)
        self.btn_anadir_contacto.clicked.connect(self.anadir_contacto)
        
        # Conexión interna de botones
        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_guardar.clicked.connect(self.procesar_guardado) 

    def anadir_enfermedad(self):
        enfermedad = self.text_Enfermedad.text().strip()
        if enfermedad:
            self.lista_enfermedades.addItem(enfermedad)
            self.text_Enfermedad.clear()

    def anadir_contacto(self):
        columna_actual = self.Familiares.columnCount()
        self.Familiares.insertColumn(columna_actual)
        self.Familiares.setItem(0, columna_actual, QTableWidgetItem(""))
        self.Familiares.setItem(1, columna_actual, QTableWidgetItem(""))
        self.Familiares.setItem(2, columna_actual, QTableWidgetItem(""))

    def obtener_datos_formulario(self) -> dict:
        datos = {
            "nombre": self.texto_NombreCompleto.text().strip(),
            "nombreUsuario": self.text_Usuario.text().strip(),
            "dni": self.text_DNI.text().strip(),
            "fechaNacimiento": self.date_Nacimiento.date().toString("yyyy-MM-dd"),
            "telefono": self.text_Telefono.text().strip(),
            "email": self.text_Email.text().strip(),
            "password": self.text_password.text().strip(),
            "tipoPaciente": self.combo_tipo.currentText().strip(),
            "cuentaBancaria": self.text_Cuenta_Bancaria.text().strip()
        }
        
        enfermedades = []
        for i in range(self.lista_enfermedades.count()):
            enfermedades.append(self.lista_enfermedades.item(i).text())
        datos["enfermedades"] = enfermedades

        familiares = []
        for col in range(self.Familiares.columnCount()):
            nombre_fam = self.Familiares.item(0, col).text().strip() if self.Familiares.item(0, col) else ""
            parentesco = self.Familiares.item(1, col).text().strip() if self.Familiares.item(1, col) else ""
            tlf_fam = self.Familiares.item(2, col).text().strip() if self.Familiares.item(2, col) else ""
            if nombre_fam:
                familiares.append({"nombre": nombre_fam, "parentesco": parentesco, "telefono": tlf_fam})
        datos["familiares"] = familiares
        
        return datos

    def procesar_guardado(self):
        raw_datos = self.obtener_datos_formulario()
        
        # El controlador mapea el tipo de paciente y la cuenta bancaria
        exito_p, msg_p, nuevo_paciente = self.controlador.agregar_paciente(raw_datos)
        
        if exito_p and nuevo_paciente:
            username_creado = nuevo_paciente.nombreUsuario
            
            for enf in raw_datos["enfermedades"]:
                _, _, enf_id = self.controlador.agregar_enfermedad(enf)
                if enf_id:
                    self.controlador.asignar_enfermedad_a_paciente(username_creado, enf_id)
            
            for fam in raw_datos["familiares"]:
                datos_fam = {"paciente": username_creado, "nombre": fam["nombre"], "parentesco": fam["parentesco"], "telefono": fam["telefono"]}
                self.controlador.agregar_familiar(datos_fam)
                
            QMessageBox.information(self, "Éxito", f"Paciente '{raw_datos['nombre']}' registrado correctamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error de Validación", f"No se pudo guardar: {msg_p}")