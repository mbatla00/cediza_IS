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
        
        self.showMaximized()
        
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
        # AHORA AÑADE UNA FILA HACIA ABAJO
        fila_actual = self.Familiares.rowCount()
        self.Familiares.insertRow(fila_actual)
        
        # Rellena la fila nueva con casillas en blanco para que puedas escribir
        self.Familiares.setItem(fila_actual, 0, QTableWidgetItem(""))
        self.Familiares.setItem(fila_actual, 1, QTableWidgetItem(""))
        self.Familiares.setItem(fila_actual, 2, QTableWidgetItem(""))

    def obtener_datos_formulario(self) -> dict:
        datos = {
            "nombre": self.texto_NombreCompleto.text().strip(),
            "nombreUsuario": self.text_Usuario.text().strip(),
            "dni": self.text_DNI.text().strip(),
            "fechaNacimiento": self.date_Nacimiento.date().toString("yyyy-MM-dd"),
            "telefono": self.text_Telefono.text().strip(),
            "email": self.text_email.text().strip(),
            "password": self.text_password.text().strip(),
            "tipoPaciente": self.tipo.currentText().strip(),
            "cuentaBancaria": self.text_Cuenta_Bancaria.text().strip() if hasattr(self, 'text_Cuenta_Bancaria') else ""
        }
        
        enfermedades = []
        for i in range(self.lista_enfermedades.count()):
            enfermedades.append(self.lista_enfermedades.item(i).text())
        datos["enfermedades"] = enfermedades

        familiares = []
        # AHORA LEE LOS DATOS RECORRIENDO LAS FILAS HACIA ABAJO
        for fila in range(self.Familiares.rowCount()):
            nombre_fam = self.Familiares.item(fila, 0).text().strip() if self.Familiares.item(fila, 0) else ""
            parentesco = self.Familiares.item(fila, 1).text().strip() if self.Familiares.item(fila, 1) else ""
            tlf_fam = self.Familiares.item(fila, 2).text().strip() if self.Familiares.item(fila, 2) else ""
            
            if nombre_fam: # Solo lo añade si has escrito un nombre
                familiares.append({"nombre": nombre_fam, "parentesco": parentesco, "telefono": tlf_fam})
        datos["familiares"] = familiares
        
        return datos

    def procesar_guardado(self):
        raw_datos = self.obtener_datos_formulario()
        
        # El controlador ahora nos devuelve directamente el string de username_creado
        exito_p, msg_p, username_creado = self.controlador.agregar_paciente(raw_datos)
        
        if exito_p and username_creado:
            # Usamos la string devuelta sin tener que acceder a propiedades de un objeto
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